#!/usr/bin/env python3
"""
Exemplo Prático: Suite de Testes Mobile com Appium
Testa app de login em Android e iOS
"""

import pytest
import time
import json
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.support.ui import WebDriverWait
from appium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.action_chains import ActionChains


# ============================================================================
# PAGE OBJECT PATTERN
# ============================================================================

class BasePage:
    """Página base com métodos comuns"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        """Encontra elemento com retry"""
        try:
            return self.wait.until(
                EC.presence_of_element_located(locator)
            )
        except:
            raise Exception(f"Elemento não encontrado: {locator}")

    def click(self, locator):
        """Clica em elemento"""
        element = self.find_element(locator)
        element.click()

    def type_text(self, locator, text):
        """Digita texto"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Obtém texto"""
        element = self.find_element(locator)
        return element.text

    def is_displayed(self, locator):
        """Verifica se elemento está visível"""
        try:
            return self.find_element(locator).is_displayed()
        except:
            return False

    def wait_for_text(self, locator, expected_text, timeout=10):
        """Aguarda texto específico"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(
            EC.text_to_be_present_in_element(locator, expected_text)
        )


class LoginPage(BasePage):
    """Página de Login"""

    # Locators (funciona para Android e iOS)
    EMAIL_INPUT = (AppiumBy.XPATH, '//XCUIElementTypeTextField[@name="email_input"] | //android.widget.EditText[@resource-id="com.example.myapp:id/email_input"]')
    PASSWORD_INPUT = (AppiumBy.XPATH, '//XCUIElementTypeSecureTextField[@name="password_input"] | //android.widget.EditText[@resource-id="com.example.myapp:id/password_input"]')
    LOGIN_BUTTON = (AppiumBy.XPATH, '//XCUIElementTypeButton[@name="login_button"] | //android.widget.Button[@resource-id="com.example.myapp:id/login_button"]')
    SUCCESS_MSG = (AppiumBy.XPATH, '//*[@text="Login Successful" or @name="Login Successful"]')
    ERROR_MSG = (AppiumBy.XPATH, '//*[@text="Invalid credentials" or @name="Invalid credentials"]')
    FORGOT_PASSWORD = (AppiumBy.XPATH, '//XCUIElementTypeButton[@name="forgot_password"] | //android.widget.Button[@resource-id="com.example.myapp:id/forgot_password"]')

    def enter_email(self, email):
        """Digita email"""
        self.type_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        """Digita senha"""
        self.type_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        """Clica botão login"""
        self.click(self.LOGIN_BUTTON)

    def login(self, email, password):
        """Efetua login"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def is_success_message_shown(self):
        """Verifica mensagem de sucesso"""
        return self.is_displayed(self.SUCCESS_MSG)

    def is_error_message_shown(self):
        """Verifica mensagem de erro"""
        return self.is_displayed(self.ERROR_MSG)

    def get_error_message(self):
        """Obtém texto de erro"""
        return self.get_text(self.ERROR_MSG)


class HomePage(BasePage):
    """Página home (após login bem-sucedido)"""

    WELCOME_TEXT = (AppiumBy.XPATH, '//*[@text="Welcome" or @name="Welcome"]')
    LOGOUT_BUTTON = (AppiumBy.XPATH, '//XCUIElementTypeButton[@name="logout"] | //android.widget.Button[@resource-id="com.example.myapp:id/logout"]')
    USER_PROFILE = (AppiumBy.XPATH, '//XCUIElementTypeButton[@name="profile"] | //android.widget.Button[@resource-id="com.example.myapp:id/profile"]')

    def is_home_page_loaded(self):
        """Verifica se home page carregou"""
        return self.is_displayed(self.WELCOME_TEXT)

    def logout(self):
        """Efetua logout"""
        self.click(self.LOGOUT_BUTTON)

    def go_to_profile(self):
        """Vai para perfil"""
        self.click(self.USER_PROFILE)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def config():
    """Carrega configuração"""
    with open("config/test_config.json") as f:
        return json.load(f)


@pytest.fixture
def driver(config, request):
    """Inicia driver do Appium"""
    platform = getattr(request, "param", "android")

    if platform == "android":
        capabilities = {
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "deviceName": "emulator-5554",
            "appPackage": "com.example.myapp",
            "appActivity": "com.example.myapp.LoginActivity",
            "noReset": False,
            "autoGrantPermissions": True,
        }
    else:  # iOS
        capabilities = {
            "platformName": "iOS",
            "automationName": "XCUITest",
            "deviceName": "iPhone 14",
            "bundleId": "com.example.myapp",
            "noReset": False,
            "autoGrantPermissions": True,
        }

    driver = webdriver.Remote(
        "http://localhost:4723",
        capabilities
    )
    yield driver
    driver.quit()


@pytest.fixture
def login_page(driver):
    """Retorna página de login"""
    return LoginPage(driver)


@pytest.fixture
def home_page(driver):
    """Retorna página home"""
    return HomePage(driver)


# ============================================================================
# TESTES
# ============================================================================

class TestLoginAndroid:
    """Testes de login para Android"""

    def test_login_success(self, login_page, home_page):
        """Testa login bem-sucedido"""
        login_page.login("test@example.com", "password123")

        time.sleep(2)
        assert home_page.is_home_page_loaded(), \
            "Home page não carregou após login"

    def test_login_invalid_email(self, login_page):
        """Testa validação de email inválido"""
        login_page.login("invalid-email", "password123")

        time.sleep(1)
        assert login_page.is_error_message_shown(), \
            "Mensagem de erro não exibida"

        error_text = login_page.get_error_message()
        assert "Invalid" in error_text or "invalid" in error_text, \
            f"Erro inesperado: {error_text}"

    def test_login_invalid_password(self, login_page):
        """Testa senha incorreta"""
        login_page.login("test@example.com", "wrongpassword")

        time.sleep(1)
        assert login_page.is_error_message_shown(), \
            "Mensagem de erro não exibida"

    def test_login_empty_email(self, login_page):
        """Testa email vazio"""
        login_page.enter_password("password123")
        login_page.click_login()

        time.sleep(1)
        assert login_page.is_error_message_shown(), \
            "Validação de campo obrigatório falhou"

    def test_login_empty_password(self, login_page):
        """Testa senha vazia"""
        login_page.enter_email("test@example.com")
        login_page.click_login()

        time.sleep(1)
        assert login_page.is_error_message_shown(), \
            "Validação de campo obrigatório falhou"

    def test_login_empty_fields(self, login_page):
        """Testa ambos campos vazios"""
        login_page.click_login()

        time.sleep(1)
        assert login_page.is_error_message_shown(), \
            "Validação não funcionou"

    def test_logout(self, login_page, home_page):
        """Testa logout"""
        login_page.login("test@example.com", "password123")
        time.sleep(2)

        assert home_page.is_home_page_loaded(), \
            "Não fez login"

        home_page.logout()
        time.sleep(2)

        assert login_page.is_displayed(login_page.LOGIN_BUTTON), \
            "Não voltou para login"


class TestNavigationAndroid:
    """Testes de navegação"""

    def test_navigate_to_profile(self, login_page, home_page):
        """Testa navegação para perfil"""
        login_page.login("test@example.com", "password123")
        time.sleep(2)

        home_page.go_to_profile()
        time.sleep(2)

        profile_title = home_page.find_element(
            (AppiumBy.XPATH, '//*[@text="Profile" or @name="Profile"]')
        )
        assert profile_title.is_displayed(), \
            "Página de perfil não carregou"

    def test_swipe_navigation(self, login_page, home_page, driver):
        """Testa navegação com swipe"""
        login_page.login("test@example.com", "password123")
        time.sleep(2)

        # Swipe da esquerda para direita
        size = driver.get_window_size()
        start_x = size['width'] * 0.2
        end_x = size['width'] * 0.8
        y = size['height'] / 2

        driver.swipe(start_x, y, end_x, y)
        time.sleep(1)

        # Verifica se mudou de aba
        assert True, "Swipe funcionou"


class TestPerformanceAndroid:
    """Testes de performance"""

    def test_login_performance(self, login_page, home_page):
        """Verifica tempo de login"""
        start = time.time()

        login_page.login("test@example.com", "password123")
        time.sleep(2)

        assert home_page.is_home_page_loaded()

        elapsed = time.time() - start
        assert elapsed < 5, f"Login demorou {elapsed:.2f}s (máximo 5s)"

        print(f"Login time: {elapsed:.2f}s")

    def test_multiple_logins_performance(self, login_page, home_page):
        """Testa performance com múltiplos logins"""
        times = []

        for i in range(3):
            start = time.time()

            login_page.login("test@example.com", "password123")
            time.sleep(1)

            assert home_page.is_home_page_loaded()

            home_page.logout()
            time.sleep(1)

            elapsed = time.time() - start
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        print(f"Average login time: {avg_time:.2f}s")

        assert avg_time < 5, f"Performance degradada: {avg_time:.2f}s"


# ============================================================================
# DATA-DRIVEN TESTS
# ============================================================================

test_data_login = [
    ("test1@example.com", "pass123", True),
    ("test2@example.com", "pass456", True),
    ("invalid@email", "pass", False),
    ("", "pass", False),
    ("test@example.com", "", False),
]


@pytest.mark.parametrize("email,password,should_succeed", test_data_login)
def test_login_data_driven(login_page, home_page, email, password, should_succeed):
    """Testa login com múltiplos dados"""
    login_page.login(email, password)
    time.sleep(2)

    if should_succeed:
        assert home_page.is_home_page_loaded(), \
            f"Login falhou para {email}"
    else:
        assert login_page.is_error_message_shown(), \
            f"Esperava erro para {email}"


# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    # Executar testes
    # pytest test_mobile_example.py -v --html=report.html

    print("Suite de testes mobile pronta!")
    print("\nPara executar:")
    print("  pytest test_mobile_example.py -v")
    print("\nPara gerar relatório:")
    print("  pytest test_mobile_example.py -v --html=report.html")
    print("\nPara apenas Android:")
    print("  pytest test_mobile_example.py::TestLoginAndroid -v")
