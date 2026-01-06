// Register Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/service-worker.js')
            .then((registration) => {
                console.log('✅ Service Worker registered:', registration.scope);
            })
            .catch((error) => {
                console.log('❌ Service Worker registration failed:', error);
            });
    });
}

// Install prompt
let deferredPrompt;
const installBanner = document.getElementById('installPWA');
const installButton = document.getElementById('installPWAButton');
const dismissButton = document.getElementById('dismissPWA');

window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent Chrome 67 and earlier from automatically showing the prompt
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;

    // Show install banner
    if (installBanner) {
        installBanner.style.display = 'block';

        // Install button click
        if (installButton) {
            installButton.addEventListener('click', () => {
                // Hide the banner
                installBanner.style.display = 'none';
                // Show the prompt
                deferredPrompt.prompt();
                // Wait for the user to respond to the prompt
                deferredPrompt.userChoice.then((choiceResult) => {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('User accepted the install prompt');
                    } else {
                        console.log('User dismissed the install prompt');
                    }
                    deferredPrompt = null;
                });
            });
        }

        // Dismiss button click
        if (dismissButton) {
            dismissButton.addEventListener('click', () => {
                installBanner.style.display = 'none';
                // Remember dismissal for this session
                sessionStorage.setItem('pwaPromptDismissed', 'true');
            });
        }
    }
});

// Check if app is installed
window.addEventListener('appinstalled', () => {
    console.log('✅ PWA was installed');
    if (installBanner) {
        installBanner.style.display = 'none';
    }
});

// Online/Offline detection
window.addEventListener('online', () => {
    console.log('✅ Back online');
    updateOnlineStatus(true);
});

window.addEventListener('offline', () => {
    console.log('⚠️ You are offline');
    updateOnlineStatus(false);
});

function updateOnlineStatus(isOnline) {
    const statusBar = document.getElementById('onlineStatus');
    if (statusBar) {
        if (isOnline) {
            statusBar.classList.add('hidden');
        } else {
            statusBar.classList.remove('hidden');
        }
    }
}

// iOS Install Prompt
const iosInstallBanner = document.getElementById('installPWAiOS');
const iosDismissButton = document.getElementById('dismissPWAiOS');

// Detect iOS
const isIos = () => {
    const userAgent = window.navigator.userAgent.toLowerCase();
    return /iphone|ipad|ipod/.test(userAgent);
}

// Detect if already installed (standalone mode)
const isInStandaloneMode = () => ('standalone' in window.navigator) && (window.navigator.standalone);

// Show iOS banner if on iOS and not installed
if (isIos() && !isInStandaloneMode() && !sessionStorage.getItem('pwaiOSPromptDismissed')) {
    if (iosInstallBanner) {
        // Show after a small delay
        setTimeout(() => {
            iosInstallBanner.style.display = 'block';
        }, 1000); // 1 second delay

        // Handle dismiss
        if (iosDismissButton) {
            iosDismissButton.addEventListener('click', () => {
                iosInstallBanner.style.display = 'none';
                sessionStorage.setItem('pwaiOSPromptDismissed', 'true');
            });
        }
    }
}
