class User:
    telegram_token : int
    api_token: str
    notifications_enable: bool
    new_enable: bool
    attacks_enable: bool
    everyday_enable: bool

    def __init__(self, tg_token, api) -> None:
        self.telegram_token = tg_token
        self.api_token = api
        self.notifications_enable = True
        self.new_enable = True
        self.attacks_enable = True
        self.everyday_enable = True

    def reverse_notifications(self) -> None:
        self.notifications_enable = not self.notifications_enable

    def reverse_new(self) -> None:
        self.new_enable = not self.new_enable

    def reverse_attacks(self) -> None:
        self.attacks_enable = not self.attacks_enable

    def reverse_everyday(self) -> None:
        self.everyday_enable = not self.everyday_enable