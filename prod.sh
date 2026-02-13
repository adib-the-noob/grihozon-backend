#!/bin/bash

# Production Docker Helper Script
# Usage: ./prod.sh [up|down|logs|build|restart|psql|shell]

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
${GREEN}Production Docker Helper${NC}

Usage: ./prod.sh [COMMAND] [OPTIONS]

Commands:
  up              Start all services (db, redis, api-web, celery)
  down            Stop all services
  restart         Restart all services
  build           Build images
  logs            View all container logs
  logs-api        View api-web logs only
  logs-celery     View celery logs only
  logs-db         View database logs only
  logs-redis      View redis logs only
  psql            Connect to PostgreSQL
  clean           Remove containers and volumes (WARNING: deletes data)
  shell           Open Django shell in api-web container
  status          Show service status

Environment:
  DOCKER_HOST     ${DOCKER_HOST:-unix:///var/run/docker.sock}
  Platform:       $(detect_platform)
  Compose File:   docker-compose.prod.yml

${BLUE}Important:${NC}
  - Ensure all environment variables are set in .env or exported
  - Required: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
  - Database data is persisted in volumes

${YELLOW}Service Order:${NC}
  1. PostgreSQL (db)
  2. Redis
  3. API Web (depends on db & redis)
  4. Celery Worker (depends on api-web & redis)

EOF
}

# Execute docker-compose command with production file
run_docker_compose() {
  docker-compose -f docker-compose.prod.yml "$@"
}

# Check environment variables
check_env_vars() {
  local required_vars=("POSTGRES_DB" "POSTGRES_USER" "POSTGRES_PASSWORD")
  local missing=false

  for var in "${required_vars[@]}"; do
    if [[ -z "${!var}" ]]; then
      echo -e "${YELLOW}Warning: $var is not set${NC}"
      missing=true
    fi
  done

  if [[ "$missing" == true ]]; then
    echo -e "${YELLOW}Using default values. Set environment variables to override.${NC}"
  fi
}

# Show service status
show_status() {
  echo -e "${BLUE}Service Status:${NC}"
  run_docker_compose ps
  echo
  echo -e "${BLUE}Container Health:${NC}"
  docker ps --format "table {{.Names}}\t{{.Status}}" --filter label=com.docker.compose.project=
}

# Main command handler
main() {
  local command="${1:-up}"

  case "$command" in
    up)
      check_env_vars
      echo -e "${GREEN}Starting production services...${NC}"
      echo -e "${BLUE}Service startup order: PostgreSQL → Redis → API Web → Celery${NC}"
      run_docker_compose up -d
      echo -e "${GREEN}✓ Services started${NC}"
      sleep 2
      show_status
      ;;
    down)
      echo -e "${YELLOW}Stopping production services...${NC}"
      read -p "Continue? (y/n) " -n 1 -r
      echo
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_docker_compose down
        echo -e "${GREEN}✓ Services stopped${NC}"
      fi
      ;;
    restart)
      echo -e "${YELLOW}Restarting production services...${NC}"
      run_docker_compose restart
      echo -e "${GREEN}✓ Services restarted${NC}"
      ;;
    build)
      echo -e "${GREEN}Building production images...${NC}"
      run_docker_compose build --no-cache
      echo -e "${GREEN}✓ Images built${NC}"
      ;;
    logs)
      run_docker_compose logs -f
      ;;
    logs-api)
      run_docker_compose logs -f api-web
      ;;
    logs-celery)
      run_docker_compose logs -f celery
      ;;
    logs-db)
      run_docker_compose logs -f db
      ;;
    logs-redis)
      run_docker_compose logs -f redis
      ;;
    psql)
      echo -e "${GREEN}Connecting to PostgreSQL...${NC}"
      run_docker_compose exec db psql -U "${POSTGRES_USER:-postgres}" -d "${POSTGRES_DB:-grihozon}"
      ;;
    clean)
      echo -e "${RED}WARNING: This will delete all data in volumes!${NC}"
      read -p "Type 'DELETE' to confirm: " confirm
      if [[ "$confirm" == "DELETE" ]]; then
        run_docker_compose down -v
        echo -e "${GREEN}✓ All containers and volumes removed${NC}"
      else
        echo -e "${YELLOW}Cancelled${NC}"
      fi
      ;;
    shell)
      echo -e "${GREEN}Opening Django shell in api-web...${NC}"
      run_docker_compose exec api-web python manage.py shell
      ;;
    status)
      check_env_vars
      show_status
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
