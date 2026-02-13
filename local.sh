#!/bin/bash

# Local Development Docker Helper Script
# Usage: ./local.sh [up|down|logs|build|restart|psql]

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detect OS
detect_platform() {
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "linux"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macos"
  elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "windows"
  else
    echo "unknown"
  fi
}

# Check if running as root on Linux
check_sudo_linux() {
  local platform=$(detect_platform)
  if [[ "$platform" == "linux" ]]; then
    if [[ $EUID -ne 0 ]]; then
      echo -e "${YELLOW}Docker requires elevated privileges on Linux.${NC}"
      read -p "Enter your password for sudo (or press Ctrl+C to cancel): " -s password
      echo
      echo "$password" | sudo -S whoami > /dev/null 2>&1 || {
        echo -e "${RED}Incorrect password or sudo access denied.${NC}"
        exit 1
      }
      # Re-run this script with sudo
      exec sudo -S bash "$0" "$@" <<< "$password"
    fi
  fi
}

# Show usage
show_usage() {
  cat << EOF
${GREEN}Local Development Docker Helper${NC}

Usage: ./local.sh [COMMAND]

Commands:
  up              Start all services (api-web and redis)
  down            Stop all services
  restart         Restart all services
  build           Build images
  logs            View container logs
  logs-web        View api-web logs only
  logs-redis      View redis logs only
  psql            Connect to PostgreSQL (local)
  clean           Remove containers and volumes
  shell           Open Django shell

Environment:
  DOCKER_HOST     ${DOCKER_HOST:-unix:///var/run/docker.sock}
  Platform:       $(detect_platform)

EOF
}

# Execute docker-compose command
run_docker_compose() {
  docker-compose "$@"
}

# Main command handler
main() {
  local command="${1:-up}"

  case "$command" in
    up)
      echo -e "${GREEN}Starting local development services...${NC}"
      run_docker_compose up -d
      echo -e "${GREEN}✓ Services started${NC}"
      echo -e "${GREEN}API Server: http://localhost:8000${NC}"
      echo -e "${GREEN}Redis: localhost:6379${NC}"
      ;;
    down)
      echo -e "${YELLOW}Stopping services...${NC}"
      run_docker_compose down
      echo -e "${GREEN}✓ Services stopped${NC}"
      ;;
    restart)
      echo -e "${YELLOW}Restarting services...${NC}"
      run_docker_compose restart
      echo -e "${GREEN}✓ Services restarted${NC}"
      ;;
    build)
      echo -e "${GREEN}Building images...${NC}"
      run_docker_compose build --no-cache
      echo -e "${GREEN}✓ Images built${NC}"
      ;;
    logs)
      run_docker_compose logs -f
      ;;
    logs-web)
      run_docker_compose logs -f api-web
      ;;
    logs-redis)
      run_docker_compose logs -f redis
      ;;
    psql)
      echo -e "${GREEN}Connecting to PostgreSQL...${NC}"
      PGPASSWORD="${POSTGRES_PASSWORD:-postgres}" psql -h "${DB_HOST:-localhost}" \
        -U "${POSTGRES_USER:-postgres}" -d "${POSTGRES_DB:-grihozon}"
      ;;
    clean)
      read -p "Are you sure you want to remove all containers and volumes? (y/n) " -n 1 -r
      echo
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_docker_compose down -v
        echo -e "${GREEN}✓ Cleaned up${NC}"
      fi
      ;;
    shell)
      echo -e "${GREEN}Opening Django shell...${NC}"
      run_docker_compose exec api-web python manage.py shell
      ;;
    help|--help|-h)
      show_usage
      ;;
    *)
      echo -e "${RED}Unknown command: $command${NC}"
      show_usage
      exit 1
      ;;
  esac
}

# Entry point
check_sudo_linux
main "$@"
