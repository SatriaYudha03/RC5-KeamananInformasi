// Dapatkan elemen judul h1
const mainTitle = document.getElementById('main-title');
// Dapatkan elemen untuk teks deskripsi yang akan dianimasikan
const typingTextElement = document.getElementById('typing-text');
// Dapatkan elemen kursor mengetik
const typingCursorElement = document.querySelector('.typing-cursor');


// --- Parameter dan Logika untuk Efek Cahaya Dinamis Judul ---
const baseColor = 'rgba(42, 82, 190, 0.9)'; // Biru utama, opacity 90%
const accentColor = 'rgba(106, 17, 203, 0.7)'; // Ungu/Cyan untuk variasi, opacity 70%

const animationSpeed = 0.002; // Kecepatan animasi (nilai lebih besar = lebih cepat)
const maxGlow = 50; // Radius blur maksimum untuk cahaya utama
const maxSpread = 70; // Radius blur maksimum untuk cahaya yang lebih menyebar
const glowOffset = 10; // Offset bayangan teks dasar yang konstan

// Fungsi untuk memperbarui efek cahaya pada setiap frame animasi
function updateGlow(timestamp) {
    const time = timestamp * animationSpeed;

    const dynamicGlowRange = maxGlow - glowOffset;
    const glowIntensity = Math.sin(time) * (dynamicGlowRange / 2) + (dynamicGlowRange / 2) + glowOffset;

    const dynamicSpreadRange = maxSpread - glowOffset;
    const spreadIntensity = Math.cos(time * 0.7) * (dynamicSpreadRange / 2) + (dynamicSpreadRange / 2) + glowOffset;

    mainTitle.style.textShadow = `
        0 0 ${glowIntensity}px ${baseColor},
        0 0 ${spreadIntensity}px ${accentColor},
        0 0 ${glowOffset}px ${baseColor}
    `;
    requestAnimationFrame(updateGlow);
}

// Mulai animasi cahaya judul jika elemen ditemukan
if (mainTitle) {
    requestAnimationFrame(updateGlow);
} else {
    console.error("Elemen dengan ID 'main-title' tidak ditemukan. Efek cahaya tidak dapat diterapkan.");
}

// --- Parameter dan Logika untuk Animasi Mengetik ---
const fullText = "Solusi keamanan siber terbaik untuk komunikasi email Anda. Enkripsi dan dekripsi pesan dengan algoritma RC5 yang kuat.";
const typingSpeed = 50; // Kecepatan mengetik dalam milidetik per karakter (nilai lebih kecil = lebih cepat)

let charIndex = 0;

// Fungsi untuk mengetik teks karakter demi karakter
function typeText() {
    if (charIndex < fullText.length) {
        // Tambahkan karakter satu per satu ke elemen teks
        typingTextElement.textContent += fullText.charAt(charIndex);
        charIndex++;
        setTimeout(typeText, typingSpeed); // Panggil fungsi lagi setelah jeda
    } else {
        // Setelah selesai mengetik, pastikan kursor berkedip
        if (typingCursorElement) {
            typingCursorElement.style.animation = 'blink-caret 0.75s step-end infinite';
        }
    }
}

// Mulai animasi mengetik setelah halaman dimuat sepenuhnya
// Memastikan elemen ada sebelum mencoba mengaksesnya
if (typingTextElement) {
    // Sembunyikan kursor dan kosongkan teks di awal
    if (typingCursorElement) {
        typingCursorElement.style.visibility = 'visible'; // Pastikan kursor terlihat
        typingCursorElement.style.animation = 'none'; // Hentikan animasi kedip awal
    }
    typingTextElement.textContent = ''; // Kosongkan teks di awal
    setTimeout(typeText, 500); // Mulai animasi mengetik setelah jeda singkat (0.5 detik)
} else {
    console.error("Elemen dengan ID 'typing-text' tidak ditemukan. Animasi mengetik tidak dapat diterapkan.");
}
