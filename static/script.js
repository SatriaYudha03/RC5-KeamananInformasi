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
const textsToAnimate = [
    "Solusi keamanan siber terbaik untuk komunikasi email Anda. Enkripsi dan dekripsi pesan dengan algoritma RC5 yang kuat.",
    "Projek hasil kolaborasi: Dwiki(2305551001), Satria(2305551058), Rifki(2305551068), Devasya(2305551074), Septino(2305551083), Tara(2305551139)"
];

const typingSpeed = 50; // Kecepatan mengetik dalam milidetik per karakter (nilai lebih kecil = lebih cepat)
const deletingSpeed = 30; // Kecepatan menghapus dalam milidetik per karakter
const delayAfterTyping = 1500; // Jeda setelah selesai mengetik (ms)
const delayAfterDeleting = 500; // Jeda setelah selesai menghapus (ms)

let textIndex = 0; // Indeks teks saat ini dalam array textsToAnimate
let charIndex = 0;
let isDeleting = false; // State untuk melacak apakah sedang mengetik atau menghapus

// Function to handle typing and deleting animation
function typeAndDelete() {
    const currentText = textsToAnimate[textIndex]; // Teks yang sedang dianimasikan

    if (isDeleting) {
        // Mode menghapus
        if (charIndex > 0) {
            typingTextElement.textContent = currentText.substring(0, charIndex - 1);
            charIndex--;
            setTimeout(typeAndDelete, deletingSpeed);
        } else {
            // Selesai menghapus, beralih ke teks berikutnya
            isDeleting = false;
            textIndex = (textIndex + 1) % textsToAnimate.length; // Pindah ke teks berikutnya
            setTimeout(typeAndDelete, delayAfterDeleting); // Jeda sebelum mengetik lagi
        }
    } else {
        // Mode mengetik
        if (charIndex < currentText.length) {
            typingTextElement.textContent = currentText.substring(0, charIndex + 1);
            charIndex++;
            setTimeout(typeAndDelete, typingSpeed);
        } else {
            // Selesai mengetik, beralih ke mode menghapus
            isDeleting = true;
            if (typingCursorElement) {
                typingCursorElement.style.animation = 'blink-caret 0.75s step-end infinite'; // Kursor berkedip saat jeda
            }
            setTimeout(typeAndDelete, delayAfterTyping); // Jeda sebelum menghapus
        }
    }
}

// Start the typing and deleting animation
if (typingTextElement && typingCursorElement) {
    typingTextElement.textContent = ''; // Kosongkan teks di awal
    typingCursorElement.style.visibility = 'visible'; // Pastikan kursor terlihat
    // Mulai animasi setelah jeda singkat
    setTimeout(typeAndDelete, 500);
} else {
    console.error("Elemen dengan ID 'typing-text' atau class 'typing-cursor' tidak ditemukan. Animasi mengetik tidak dapat diterapkan.");
}

// --- Logika untuk Menampilkan SweetAlert dari Flash Messages ---
// This function will be called after DOMContentLoaded
function displayFlashedMessages() {
    // Check if there are flash messages passed from Flask
    if (window.flashedMessages && window.flashedMessages.length > 0) {
        window.flashedMessages.forEach(function(msg) {
            const category = msg[0]; // Category (e.g., 'success', 'error')
            let message = msg[1];   // Message text

            // ===== PERBAIKAN DI SINI: Ganti \n dengan <br> untuk SweetAlert HTML =====
            message = message.replace(/\n/g, '<br>');

            Swal.fire({
                icon: (category === "success" ? "success" : "error"), // Determine icon based on category
                title: (category === "success" ? "Berhasil!" : "Gagal!"), // Determine title
                html: message, // Gunakan 'html' sebagai pengganti 'text'
                confirmButtonText: 'OK',
                customClass: {
                    popup: 'swal-custom-popup',
                    title: 'swal-custom-title',
                    htmlContainer: 'swal-custom-html-container',
                    confirmButton: 'swal-custom-confirm-button'
                }
            });
        });
        // Clear messages from global variable after displaying to prevent duplication
        window.flashedMessages = [];
    }
}

// Call displayFlashedMessages function after DOM is loaded
// This ensures SweetAlert2 and HTML elements are ready
document.addEventListener('DOMContentLoaded', displayFlashedMessages);
