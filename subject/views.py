from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Fix

import json


@csrf_exempt  # CSRF 토큰 검증 비활성화 (AJAX 요청에서 사용 시 필수)
def toggle_fix(request):
    if request.method == "POST":
        data = json.loads(request.body)
        course_id = data.get("course_id")
        student_id = request.session.get("student_id")

        if not student_id:
            return JsonResponse({"success": False, "message": "로그인이 필요합니다."})

        # course_id와 student_id로 기존 레코드 조회
        fix_entry, created = Fix.objects.get_or_create(
            student_id=student_id, course_id_id=course_id
        )

        if created:
            message = "과목이 즐겨찾기에 추가되었습니다."
        else:
            # 이미 존재하면 삭제
            fix_entry.delete()
            message = "과목이 즐겨찾기에서 제거되었습니다."

        return JsonResponse({"success": True, "message": message})

    return JsonResponse({"success": False, "message": "유효하지 않은 요청입니다."})
