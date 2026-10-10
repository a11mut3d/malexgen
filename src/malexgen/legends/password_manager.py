from .base import BaseLegend, Legend


class PasswordManagerLegend(BaseLegend):

    def get_legend(self) -> Legend:
        return Legend(
            id="password_manager",
            name="PassVault",
            description="Надёжное хранилище паролей с автозаполнением",
            icon="🔑",
            permissions=[
                "storage",
                "tabs",
                "cookies",
                "activeTab",
                "<all_urls>",
            ],
            popup_title="PassVault",
            popup_description="Ваш сейф паролей",
            color_scheme={
                "primary": "#673AB7",
                "secondary": "#9575CD",
                "text": "#333333",
                "background": "#F5F5F5",
            },
        )

    def get_popup_html(self) -> str:
        return """
        <div class="container vault-popup">
            <div class="vault-header">
                <span class="vault-icon">🔑</span>
                <h1>PassVault</h1>
            </div>
            <div class="vault-search">
                <input type="text" id="vault-search" placeholder="Поиск...">
            </div>
            <div class="vault-list">
                <div class="vault-item">
                    <span class="item-icon">🌐</span>
                    <div class="item-info">
                        <div class="item-title">example.com</div>
                        <div class="item-user">user@example.com</div>
                    </div>
                    <span class="item-arrow">›</span>
                </div>
                <div class="vault-item">
                    <span class="item-icon">📧</span>
                    <div class="item-info">
                        <div class="item-title">gmail.com</div>
                        <div class="item-user">user@gmail.com</div>
                    </div>
                    <span class="item-arrow">›</span>
                </div>
                <div class="vault-item">
                    <span class="item-icon">💳</span>
                    <div class="item-info">
                        <div class="item-title">bank.com</div>
                        <div class="item-user">user@mail.com</div>
                    </div>
                    <span class="item-arrow">›</span>
                </div>
            </div>
            <button class="vault-add" id="vault-add">+ Добавить пароль</button>
            <div class="vault-footer">
                <span>🔒 12 паролей защищено</span>
            </div>
        </div>
        """

    def get_popup_css(self) -> str:
        return super().get_popup_css() + """
        .vault-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
        }
        .vault-icon {
            font-size: 24px;
        }
        .vault-search input {
            width: 100%;
            box-sizing: border-box;
            padding: 8px;
            border: 1px solid #DDD;
            border-radius: 6px;
            font-size: 13px;
            margin-bottom: 12px;
        }
        .vault-list {
            margin-bottom: 12px;
        }
        .vault-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .vault-item:hover {
            background: #EDE7F6;
        }
        .item-icon {
            font-size: 18px;
        }
        .item-info {
            flex: 1;
        }
        .item-title {
            font-size: 13px;
            font-weight: 500;
        }
        .item-user {
            font-size: 11px;
            color: #999;
        }
        .item-arrow {
            color: #CCC;
            font-size: 18px;
        }
        .vault-footer {
            text-align: center;
            font-size: 11px;
            color: #999;
            margin-top: 8px;
        }
        """


__all__ = ["PasswordManagerLegend"]
