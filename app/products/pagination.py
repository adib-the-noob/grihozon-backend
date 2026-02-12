from rest_framework.pagination import PageNumberPagination


class CategoryProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_meta(self):
        return {
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "page": self.page.number,
            "total_pages": self.page.paginator.num_pages,
        }

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_meta(self):
        return {
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "page": self.page.number,
            "total_pages": self.page.paginator.num_pages,
        }