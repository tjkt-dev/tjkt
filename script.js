// --- Inisialisasi Canvas dan Konteks ---
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// --- Variabel Game ---
let birdX = 50;
let birdY = 150;
let birdSize = 20;
let gravity = 0.5;
let velocity = 0;
let jumpPower = -8;
let score = 0;
let isGameOver = false;

// Array untuk menyimpan pipa (halangan)
let pipes = [];
let pipeWidth = 50;
let pipeGap = 120; // Jarak vertikal antara pipa atas dan bawah
let pipeInterval = 100; // Frekuensi pipa muncul (setiap X frame)
let frameCount = 0;

// --- Fungsi Gambar ---
function drawBird() {
    ctx.fillStyle = 'yellow';
    ctx.fillRect(birdX, birdY, birdSize, birdSize);
}

function drawPipes() {
    ctx.fillStyle = 'green';
    for (let i = 0; i < pipes.length; i++) {
        const p = pipes[i];
        // Pipa Atas
        ctx.fillRect(p.x, 0, pipeWidth, p.topHeight);
        // Pipa Bawah
        ctx.fillRect(p.x, p.topHeight + pipeGap, pipeWidth, canvas.height - (p.topHeight + pipeGap));
    }
}

function drawScore() {
    ctx.fillStyle = 'black';
    ctx.font = '24px Arial';
    ctx.fillText(`Score: ${score}`, 10, 30);
}

// --- Logika Update Game ---
function update() {
    if (isGameOver) {
        // Tampilkan pesan Game Over
        ctx.fillStyle = 'red';
        ctx.font = '48px Arial';
        ctx.fillText('GAME OVER', canvas.width / 2 - 130, canvas.height / 2);
        ctx.font = '24px Arial';
        ctx.fillText('Klik untuk Restart', canvas.width / 2 - 90, canvas.height / 2 + 40);
        return; // Hentikan game loop
    }

    // 1. Bersihkan Canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 2. Fisika Burung (Gravitasi)
    velocity += gravity;
    birdY += velocity;

    // 3. Pergerakan Pipa dan Penghapusan Pipa Lama
    for (let i = 0; i < pipes.length; i++) {
        const p = pipes[i];
        p.x -= 2; // Kecepatan pipa

        // Cek jika burung melewati pipa (menambah skor)
        if (!p.passed && p.x + pipeWidth < birdX) {
            score++;
            p.passed = true;
        }
    }

    // Hapus pipa yang sudah keluar layar
    pipes = pipes.filter(p => p.x + pipeWidth > 0);

    // 4. Tambahkan Pipa Baru
    frameCount++;
    if (frameCount % pipeInterval === 0) {
        // Tinggi pipa atas secara acak (memastikan ada ruang di atas dan di bawah)
        const minTopHeight = 50;
        const maxTopHeight = canvas.height - pipeGap - 50;
        const topHeight = Math.floor(Math.random() * (maxTopHeight - minTopHeight + 1)) + minTopHeight;

        pipes.push({
            x: canvas.width,
            topHeight: topHeight,
            passed: false // Untuk melacak apakah burung sudah melewatinya
        });
    }

    // 5. Cek Tabrakan (Collision Detection)
    // Cek Batas Atas/Bawah
    if (birdY + birdSize > canvas.height || birdY < 0) {
        isGameOver = true;
    }

    // Cek Tabrakan dengan Pipa
    for (let i = 0; i < pipes.length; i++) {
        const p = pipes[i];
        
        // Cek tabrakan di sumbu X
        if (birdX + birdSize > p.x && birdX < p.x + pipeWidth) {
            // Cek tabrakan di sumbu Y (Pipa Atas)
            if (birdY < p.topHeight) {
                isGameOver = true;
            }
            // Cek tabrakan di sumbu Y (Pipa Bawah)
            if (birdY + birdSize > p.topHeight + pipeGap) {
                isGameOver = true;
            }
        }
    }

    // 6. Gambar Semua Elemen
    drawPipes();
    drawBird();
    drawScore();

    // 7. Loop Game
    requestAnimationFrame(update);
}

// --- Event Listener (Input User) ---
function jump() {
    if (!isGameOver) {
        velocity = jumpPower; // Beri kecepatan negatif (ke atas)
    } else {
        // Restart Game
        isGameOver = false;
        birdY = 150;
        velocity = 0;
        score = 0;
        pipes = [];
        frameCount = 0;
        update(); // Mulai game loop lagi
    }
}

// Lompat saat klik mouse atau tekan spasi
document.addEventListener('mousedown', jump);
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        jump();
    }
});

// Mulai Game
update();