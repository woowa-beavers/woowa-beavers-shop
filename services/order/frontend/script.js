async function handlePayment() {
    const userId = "beaver_01"; // 실무에선 로그인 세션에서 가져옴
    const itemId = "beaver_item_01";
    const quantity = document.getElementById('quantity').value;
    const price = 50000;

    const resultElement = document.getElementById('result');
    resultElement.innerText = "결제 처리 중...";

    try {
        const response = await fetch('http://localhost:8004/api/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                item_id: itemId,
                price: price,
                quantity: parseInt(quantity)
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            resultElement.innerText = `✅ 결제 성공!\n남은 포인트: ${data.remaining_point}원`;
        } else {
            resultElement.innerText = `❌ 결제 실패: ${data.detail}`;
        }
    } catch (error) {
        resultElement.innerText = "⚠️ 서버 연결 에러 (CORS 설정을 확인하세요!)";
    }
}