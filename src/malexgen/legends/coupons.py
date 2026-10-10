from .base import BaseLegend, Legend


class CouponsLegend(BaseLegend):

    def get_legend(self) -> Legend:
        return Legend(
            id="coupons",
            name="CouponFinder",
            description="Автоматически находит купоны и скидки при покупках",
            icon="🎟️",
            permissions=[
                "storage",
                "tabs",
                "activeTab",
                "webRequest",
                "<all_urls>",
            ],
            popup_title="CouponFinder",
            popup_description="Купоны",
            color_scheme={
                "primary": "#00BCD4",
                "secondary": "#4DD0E1",
                "text": "#333333",
                "background": "#F5F5F5",
            },
        )

    def get_popup_html(self) -> str:
        return """
        <div class="container coupons-popup">
            <div class="coupons-header">
                <span class="coupons-icon">🎟️</span>
                <h1>CouponFinder</h1>
            </div>
            <div class="coupons-status">
                <span class="status-text">Найдено купонов на этой странице:</span>
                <span class="status-count" id="coupons-count">3</span>
            </div>
            <div class="coupons-list">
                <div class="coupon-item">
                    <div class="coupon-discount">-15%</div>
                    <div class="coupon-info">
                        <div class="coupon-title">Скидка на первый заказ</div>
                        <div class="coupon-code">WELCOME15</div>
                    </div>
                    <button class="coupon-copy" data-code="WELCOME15">📋</button>
                </div>
                <div class="coupon-item">
                    <div class="coupon-discount">-500₽</div>
                    <div class="coupon-info">
                        <div class="coupon-title">Бесплатная доставка</div>
                        <div class="coupon-code">FREESHIP</div>
                    </div>
                    <button class="coupon-copy" data-code="FREESHIP">📋</button>
                </div>
                <div class="coupon-item">
                    <div class="coupon-discount">-10%</div>
                    <div class="coupon-info">
                        <div class="coupon-title">На всё</div>
                        <div class="coupon-code">SAVE10</div>
                    </div>
                    <button class="coupon-copy" data-code="SAVE10">📋</button>
                </div>
            </div>
            <button class="coupons-apply" id="coupons-apply">Применить лучший</button>
            <div class="coupons-footer">
                <label>
                    <input type="checkbox" checked> Уведомлять о купонах
                </label>
            </div>
        </div>
        """

    def get_popup_css(self) -> str:
        return super().get_popup_css() + """
        .coupons-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }
        .coupons-icon {
            font-size: 24px;
        }
        .coupons-status {
            padding: 8px 10px;
            background: #E0F7FA;
            border-radius: 6px;
            margin-bottom: 12px;
            font-size: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status-count {
            font-size: 18px;
            font-weight: bold;
            color: #00BCD4;
        }
        .coupons-list {
            margin-bottom: 12px;
            max-height: 200px;
            overflow-y: auto;
        }
        .coupon-item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px;
            background: #FFF;
            border-radius: 6px;
            margin-bottom: 6px;
            border: 1px dashed #00BCD4;
        }
        .coupon-discount {
            font-size: 14px;
            font-weight: bold;
            color: #00BCD4;
            min-width: 48px;
        }
        .coupon-info {
            flex: 1;
        }
        .coupon-title {
            font-size: 11px;
            color: #666;
        }
        .coupon-code {
            font-size: 12px;
            font-weight: bold;
            font-family: monospace;
            color: #333;
        }
        .coupon-copy {
            background: transparent;
            border: none;
            cursor: pointer;
            font-size: 14px;
            width: auto;
            padding: 4px;
        }
        .coupons-footer {
            margin-top: 8px;
            font-size: 11px;
            color: #666;
        }
        """


__all__ = ["CouponsLegend"]
