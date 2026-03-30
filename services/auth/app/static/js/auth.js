// --- 1. 회원가입 로직 ---
document.getElementById('signupForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const passwordConfirm = document.getElementById('passwordConfirm').value;

  if (password !== passwordConfirm) {
    alert('비밀번호가 일치하지 않습니다.');
    return;
  }

  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  try {
    const response = await fetch('/api/auth/signup', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (response.ok) {
      alert('회원가입 성공! 로그인 페이지로 이동합니다.');
      window.location.href = '/login';
    } else {
      alert('가입 실패: ' + (data.detail || '알 수 없는 오류'));
    }
  } catch (error) {
    console.error('에러:', error);
    alert('서버와 연결할 수 없습니다.');
  }
});

// --- 2. 로그인 로직 ---
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      body: formData,
      credentials: 'include',
    });

    if (response.ok) {
      alert('로그인 성공!');
      window.location.href = '/main';
    } else {
      const data = await response.json();
      alert('로그인 실패: ' + (data.detail || '정보가 일치하지 않습니다.'));
    }
  } catch (error) {
    console.error('에러:', error);
    alert('서버와 연결할 수 없습니다.');
  }
});
