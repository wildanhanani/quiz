const installBanner = document.getElementById('installPWA');
const installButton = document.getElementById('installPWAButton');
const dismissButton = document.getElementById('dismissPWA');
const iosInstallBanner = document.getElementById('installPWAiOS');
const iosDismissButton = document.getElementById('dismissPWAiOS');
const onlineStatus = document.getElementById('onlineStatus');

let deferredPrompt = null;

const isIos = () => /iphone|ipad|ipod/.test(window.navigator.userAgent.toLowerCase());
const isStandalone = () => window.matchMedia('(display-mode: standalone)').matches
    || (window.navigator.standalone === true);

const showElement = (element) => {
    if (element) {
        element.style.display = 'block';
    }
};

const hideElement = (element) => {
    if (element) {
        element.style.display = 'none';
    }
};

const updateOnlineStatus = (isOnline) => {
    if (!onlineStatus) {
        return;
    }

    if (isOnline) {
        onlineStatus.classList.add('hidden');
    } else {
        onlineStatus.classList.remove('hidden');
    }
};

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/service-worker.js', { scope: '/' })
            .catch(() => null);
    });
}

window.addEventListener('beforeinstallprompt', (event) => {
    event.preventDefault();
    deferredPrompt = event;

    if (isStandalone() || sessionStorage.getItem('pwaPromptDismissed')) {
        return;
    }

    showElement(installBanner);
});

if (installButton) {
    installButton.addEventListener('click', async () => {
        if (!deferredPrompt) {
            return;
        }

        hideElement(installBanner);
        deferredPrompt.prompt();
        await deferredPrompt.userChoice;
        deferredPrompt = null;
    });
}

if (dismissButton) {
    dismissButton.addEventListener('click', () => {
        sessionStorage.setItem('pwaPromptDismissed', 'true');
        hideElement(installBanner);
    });
}

window.addEventListener('appinstalled', () => {
    deferredPrompt = null;
    hideElement(installBanner);
    hideElement(iosInstallBanner);
});

window.addEventListener('online', () => updateOnlineStatus(true));
window.addEventListener('offline', () => updateOnlineStatus(false));
updateOnlineStatus(window.navigator.onLine);

if (isIos() && !isStandalone() && !sessionStorage.getItem('pwaiOSPromptDismissed')) {
    window.setTimeout(() => showElement(iosInstallBanner), 1000);
}

if (iosDismissButton) {
    iosDismissButton.addEventListener('click', () => {
        sessionStorage.setItem('pwaiOSPromptDismissed', 'true');
        hideElement(iosInstallBanner);
    });
}
