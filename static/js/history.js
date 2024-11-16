// 폼 제출 시 동작할 함수
document
  .getElementById("subject-form")
  .addEventListener("submit", function (event) {
    // event.preventDefault();

    const inputField = document.getElementById("subject");
    const inputValue = inputField.value.trim();

    if (inputValue !== "") {
      // 새로운 과목 항목 생성
      const newSubject = document.createElement("div");
      newSubject.className =
        "subject-item flex justify-between items-center p-2 bg-green-50 border border-green-200 rounded-md shadow-sm";
      newSubject.textContent = inputValue;

      // 삭제 버튼 추가
      const deleteBtn = document.createElement("button");
      deleteBtn.className =
        "delete-btn text-red-500 text-lg px-1 hover:text-red-700 transition-colors";
      deleteBtn.innerHTML = "×"; // '×' 기호로 표시
      deleteBtn.onclick = async function () {
        // 서버로 삭제 요청
        const response = await fetch("/history/", {
          method: "DELETE",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken(), // CSRF 토큰 추가
              "X-Custom-Type": "delete", // 요청 구분을 위한 커스텀 헤더
          },
          body: JSON.stringify({ course_title : subjectItem.textContent }),
        });

        if (response.ok) {
            const result = await response.json();
            if (result.success) {
                subjectItem.remove(); // 성공 시 항목 삭제
                alert("삭제되었습니다.");
            } else {
                alert("삭제 실패: " + result.message);
            }
        } else {
            alert("서버 오류로 삭제할 수 없습니다.");
        }
      };

      // 항목에 삭제 버튼 추가
      newSubject.appendChild(deleteBtn);

      // 생성된 항목을 subject-list에 추가
      document.getElementById("cert-subject-list").appendChild(newSubject);

      // 입력 필드 초기화
      setTimeout(() => {
        document.getElementById("subject-form").reset();
      }, 100);
    } else {
      alert("과목을 입력해주세요!");
    }
  });
