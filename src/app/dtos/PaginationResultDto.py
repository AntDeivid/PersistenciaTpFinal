from pydantic import BaseModel


class PaginationResultDto(BaseModel):
    page: int
    limit: int
    total_items: int
    number_of_pages: int
    data: list