from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from .models import Fix, SkkuSubject

import json


def toggle_fix(request):
    if request.method == "POST":
        student_id = request.session.get("student_id")
        data = json.loads(request.body)
        course_id = data.get("course_id")

        if not student_id:
            return JsonResponse({"success": False, "message": "로그인이 필요합니다."})

        # SkkuSubject 인스턴스 가져오기
        course = get_object_or_404(SkkuSubject, course_id=course_id)

        # Fix 존재 여부 확인 후 추가/삭제 처리
        if Fix.objects.filter(student_id=student_id, course_id=course).exists():
            Fix.objects.filter(student_id=student_id, course_id=course).delete()
            action = "removed"
            message = "즐겨찾기에서 삭제되었습니다."
        else:
            Fix.objects.create(student_id=student_id, course_id=course)
            action = "added"
            message = "즐겨찾기에 추가되었습니다."

        return JsonResponse({"success": True, "action": action, "message": message})
    return JsonResponse({"success": False, "message": "잘못된 요청입니다."})
