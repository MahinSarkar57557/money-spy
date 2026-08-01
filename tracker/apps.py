from django.apps import AppConfig


class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    def ready(self):
        try:
            from tracker.models import Category
            
            all_categories = [
                # --- Expense Categories (is_income = False) [গুরুত্বপূর্ণগুলো একদম উপরে থাকবে] ---
                {"name": "Food & Snacks", "icon": "fas fa-utensils", "color": "#FF5733", "is_income": False},
                {"name": "Rent & Mess Bill", "icon": "fas fa-home", "color": "#3357FF", "is_income": False},
                {"name": "Transport & Commute", "icon": "fas fa-bus", "color": "#33FF57", "is_income": False},
                {"name": "Study & Stationery", "icon": "fas fa-book", "color": "#33FFF0", "is_income": False},
                {"name": "University Fee", "icon": "fas fa-graduation-cap", "color": "#FF8333", "is_income": False},
                {"name": "Clothing", "icon": "fas fa-tshirt", "color": "#E91E63", "is_income": False},
                {"name": "Shopping", "icon": "fas fa-shopping-bag", "color": "#FF3383", "is_income": False},
                
                # --- অন্যান্য এক্সপেন্স ক্যাটাগরি ---
                {"name": "Utilities (Gas/Electricity)", "icon": "fas fa-bolt", "color": "#F3FF33", "is_income": False},
                {"name": "Internet & Mobile", "icon": "fas fa-wifi", "color": "#FF33F3", "is_income": False},
                {"name": "Tuition & Coaching", "icon": "fas fa-chalkboard-teacher", "color": "#8333FF", "is_income": False},
                {"name": "Hair Cut & Grooming", "icon": "fas fa-cut", "color": "#33FF83", "is_income": False},
                {"name": "Health & Medical", "icon": "fas fa-medkit", "color": "#FF3333", "is_income": False},
                {"name": "Tea & Coffee", "icon": "fas fa-coffee", "color": "#D4AC0D", "is_income": False},
                {"name": "Laundry & Iron", "icon": "fas fa-tshirt", "color": "#5D6D7E", "is_income": False},
                {"name": "Entertainment & Movies", "icon": "fas fa-film", "color": "#AF7AC5", "is_income": False},
                {"name": "Tour & Travel", "icon": "fas fa-plane", "color": "#48C9B0", "is_income": False},
                {"name": "bKash / Nagad Cashout", "icon": "fas fa-wallet", "color": "#EC7063", "is_income": False},
                {"name": "Debt Repayment", "icon": "fas fa-hand-holding-usd", "color": "#5499C7", "is_income": False},
                {"name": "Savings & Deposit", "icon": "fas fa-piggy-bank", "color": "#52BE80", "is_income": False},
                {"name": "Emergency Fund", "icon": "fas fa-shield-alt", "color": "#F4D03F", "is_income": False},
                {"name": "Online Payment", "icon": "fas fa-credit-card", "color": "#00BCD4", "is_income": False},
                {"name": "Course", "icon": "fas fa-laptop", "color": "#673AB7", "is_income": False},
                {"name": "App Subscription", "icon": "fas fa-mobile", "color": "#3F51B5", "is_income": False},
                {"name": "Repairing", "icon": "fas fa-tools", "color": "#795548", "is_income": False},
                {"name": "Gift", "icon": "fas fa-gift", "color": "#E91E63", "is_income": False},
                {"name": "Donation", "icon": "fas fa-hand-holding-heart", "color": "#009688", "is_income": False},
                {"name": "Other Expenses", "icon": "fas fa-ellipsis-h", "color": "#95A5A6", "is_income": False},

                # --- Income Categories (is_income = True) [এগুলো শুধুমাত্র ইনকাম পেজে দেখাবে] ---
                {"name": "Job Salary", "icon": "fas fa-briefcase", "color": "#2980B9", "is_income": True},
                {"name": "Scholarship", "icon": "fas fa-award", "color": "#27AE60", "is_income": True},
                {"name": "Freelancing", "icon": "fas fa-laptop-code", "color": "#3498DB", "is_income": True},
                {"name": "Tuition Income", "icon": "fas fa-book-reader", "color": "#28B463", "is_income": True},
                {"name": "Pocket Money", "icon": "fas fa-coins", "color": "#1ABC9C", "is_income": True},
                {"name": "Business Income", "icon": "fas fa-store", "color": "#9B59B6", "is_income": True},
                {"name": "Online Sales", "icon": "fas fa-shopping-cart", "color": "#E67E22", "is_income": True},
                {"name": "Investment", "icon": "fas fa-chart-line", "color": "#2E4053", "is_income": True},
                {"name": "Dividend / Profit", "icon": "fas fa-hand-holding-heart", "color": "#27AE60", "is_income": True},
                {"name": "Money Back / Return", "icon": "fas fa-undo-alt", "color": "#16A085", "is_income": True},
                {"name": "Other Income", "icon": "fas fa-plus-circle", "color": "#7F8C8D", "is_income": True}
            ]

            for item in all_categories:
                obj, created = Category.objects.get_or_create(name=item["name"])
                obj.icon = item["icon"]
                obj.color = item["color"]
                obj.is_income = item["is_income"]
                obj.save()
        except Exception:
            pass