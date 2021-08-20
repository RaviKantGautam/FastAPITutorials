from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Todo(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    description = fields.TextField(blank=True)

    class PydanticMeta:
        pass

Todo_Pydantic = pydantic_model_creator(Todo, name="Todo")
TodoIn_Pydantic = pydantic_model_creator(Todo, name="TodoIn", exclude_readonly=True)