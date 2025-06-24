const video = document.getElementById('video');
navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
  .then(stream => video.srcObject = stream)
  .catch(err => alert("ไม่สามารถเข้าถึงกล้อง: " + err));

function captureAndSend() {
  const canvas = document.getElementById('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  const imageData = canvas.toDataURL('image/png');

  fetch('/count', {
    method: 'POST',
    body: JSON.stringify({ image: imageData }),
    headers: { 'Content-Type': 'application/json' }
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('result').innerText = `จำนวนเม็ดยา: ${data.count}`;
  });
}