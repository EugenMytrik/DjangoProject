from django.http import JsonResponse, HttpResponseBadRequest
from faker import Faker
from .models import Student


def generate_student(request):
    fake = Faker()
    student_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=30),
    }
    student = Student.objects.create(**student_data)
    response_data = {
        "id": student.id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "birth_date": student.birth_date.strftime("%Y-%m-%d"),
    }
    return JsonResponse(response_data)


def generate_students(request):
    try:
        count = int(request.GET.get("count", 1))
        if count < 1 or count > 100:
            raise ValueError("Count should be a positive integer between 1 and 100")
    except ValueError as e:
        return HttpResponseBadRequest(str(e))

    fake = Faker()
    students_data = []
    for _ in range(count):
        student_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=30),
        }
        students_data.append(student_data)

    students = Student.objects.bulk_create([Student(**data) for data in students_data])
    response_data = [
        {
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "birth_date": student.birth_date.strftime("%Y-%m-%d"),
        }
        for student in students
    ]

    return JsonResponse(response_data, safe=False)
