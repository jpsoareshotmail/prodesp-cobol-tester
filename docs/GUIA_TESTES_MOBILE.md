# Guia Completo: Automação de Testes Mobile (Android & iOS)

## Índice
1. Frameworks e Ferramentas
2. Estratégia de Testes
3. Setup e Instalação
4. Exemplos Práticos
5. Best Practices
6. CI/CD para Mobile

---

## 1. Frameworks e Ferramentas

### 1.1 Principais Opções

| Framework | Linguagem | Android | iOS | Cross-platform |
|-----------|-----------|---------|-----|-----------------|
| **Appium** | Java, Python, JS | ✅ | ✅ | ✅ (Melhor) |
| **Espresso** | Java, Kotlin | ✅ | ❌ | ❌ |
| **XCUITest** | Swift | ❌ | ✅ | ❌ |
| **Calabash** | Ruby | ✅ | ✅ | ✅ |
| **Detox** | JS | ✅ | ✅ | ✅ (React Native) |
| **Robot Framework** | Python | ✅ | ✅ | ✅ |

### 1.2 Recomendações por Cenário

**Para Apps Nativas Android**
```
Melhor: Espresso (nativo, rápido)
Alternativa: Appium (cross-platform)
```

**Para Apps Nativas iOS**
```
Melhor: XCUITest (nativo, rápido)
Alternativa: Appium (cross-platform)
```

**Para Apps Cross-Platform (Android + iOS)**
```
Melhor: Appium (compatível com ambos)
Alternativa: Calabash, Detox
```

**Para Apps React Native/Flutter**
```
Melhor: Detox (React Native) / Flutter Driver (Flutter)
Alternativa: Appium
```

---

## 2. Estratégia de Testes Mobile

### 2.1 Piramide de Testes

```
              Manual Tests (Exploratória)
              ↑
            UI Tests (E2E) - 15%
            ↑
        Integration Tests - 25%
        ↑
    Unit Tests - 60%
    ↑
(Mais rápido, menos custoso)
```

### 2.2 Tipos de Testes

#### A. Unit Tests
```
Teste: Lógica de negócio isolada
Ferramenta: JUnit (Android), XCTest (iOS)
Tempo: < 100ms
Cobertura: 60% do código
```

#### B. Integration Tests
```
Teste: Múltiplos componentes juntos
Ferramenta: Appium, Calabash
Tempo: 1-5 segundos
Cobertura: 25% do código
```

#### C. UI/E2E Tests
```
Teste: Fluxo completo do usuário
Ferramenta: Appium, Espresso, XCUITest
Tempo: 5-30 segundos
Cobertura: 15% do código
```

### 2.3 Áreas de Teste

```
✓ Login/Autenticação
✓ Navegação
✓ Formulários
✓ Offline Mode
✓ Push Notifications
✓ Câmera/Galeria
✓ Permissões
✓ Performance
✓ Bateria/Memória
✓ Compatibilidade (versões)
```

---

## 3. Setup e Instalação

### 3.1 Appium (Recomendado para Cross-Platform)

#### Instalação

```bash
# Instalar Node.js (se não tiver)
# https://nodejs.org

# Instalar Appium globalmente
npm install -g appium

# Instalar Appium Doctor (verificar setup)
npm install -g appium-doctor

# Verificar instalação
appium --version
appium-doctor
```

#### Pré-requisitos

**Android**
```bash
# Android SDK
export ANDROID_HOME=/path/to/android-sdk
export PATH=$PATH:$ANDROID_HOME/bin

# Ferramentas necessárias
- SDK Platform Tools
- Build Tools
- Emulator
- API Level 28+ (recomendado)

# ADB (Android Debug Bridge)
adb devices
```

**iOS**
```bash
# Xcode
xcode-select --install

# Xcodes (gerenciador de versões)
brew install xcodes

# iOS Deploy
npm install -g ios-deploy

# Verifica Xcode
xcode-select -p
```

### 3.2 Espresso (Android Nativo)

```gradle
// build.gradle (Android)
androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
androidTestImplementation 'androidx.test:runner:1.5.2'
androidTestImplementation 'androidx.test:rules:1.5.0'
```

### 3.3 XCUITest (iOS Nativo)

```
// Já vem integrado no Xcode
// Menu: Editor → Add Build Phase → New Run Script Phase
```

---

## 4. Exemplos Práticos

### 4.1 Appium com Python

#### Setup Inicial

```python
# requirements.txt
appium-python-client==2.9.0
pytest==7.4.0
pytest-xdist==3.3.1
```

#### Exemplo 1: Teste de Login (Android)

```python
import pytest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.appium_service import AppiumService
import time

class TestLoginAndroid:
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Inicia driver do Appium"""
        capabilities = {
            'platformName': 'Android',
            'automationName': 'UiAutomator2',
            'deviceName': 'emulator-5554',  # ou nome real do device
            'appPackage': 'com.example.myapp',
            'appActivity': 'com.example.myapp.LoginActivity',
            'noReset': False,
        }
        
        driver = webdriver.Remote(
            'http://localhost:4723',
            capabilities
        )
        yield driver
        driver.quit()
    
    def test_login_success(self, driver):
        """Testa login bem-sucedido"""
        # Encontrar elementos
        email_field = driver.find_element(
            AppiumBy.ID, 
            'com.example.myapp:id/email_input'
        )
        password_field = driver.find_element(
            AppiumBy.ID,
            'com.example.myapp:id/password_input'
        )
        login_button = driver.find_element(
            AppiumBy.ID,
            'com.example.myapp:id/login_button'
        )
        
        # Preencher dados
        email_field.send_keys('test@example.com')
        password_field.send_keys('password123')
        
        # Clicar
        login_button.click()
        
        # Validar
        time.sleep(2)
        success_msg = driver.find_element(
            AppiumBy.XPATH,
            '//*[@text="Login Successful"]'
        )
        assert success_msg.is_displayed()
    
    def test_login_invalid_email(self, driver):
        """Testa validação de email inválido"""
        email_field = driver.find_element(
            AppiumBy.ID,
            'com.example.myapp:id/email_input'
        )
        login_button = driver.find_element(
            AppiumBy.ID,
            'com.example.myapp:id/login_button'
        )
        
        email_field.send_keys('invalid-email')
        login_button.click()
        
        time.sleep(1)
        error_msg = driver.find_element(
            AppiumBy.XPATH,
            '//*[@text="Invalid email format"]'
        )
        assert error_msg.is_displayed()
    
    def test_login_empty_fields(self, driver):
        """Testa campos vazios"""
        login_button = driver.find_element(
            AppiumBy.ID,
            'com.example.myapp:id/login_button'
        )
        login_button.click()
        
        time.sleep(1)
        error_msg = driver.find_element(
            AppiumBy.XPATH,
            '//*[@text="Please fill all fields"]'
        )
        assert error_msg.is_displayed()
```

#### Exemplo 2: Teste com Swipe e Scroll

```python
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains

def test_swipe_navigation(driver):
    """Testa navegação com gestos"""
    
    # Swipe da esquerda para direita
    size = driver.get_window_size()
    start_x = size['width'] * 0.2
    end_x = size['width'] * 0.8
    y = size['height'] / 2
    
    driver.swipe(start_x, y, end_x, y)
    time.sleep(1)
    
    # Scroll para baixo
    driver.execute_script(
        'mobile: scrollGesture',
        {
            'left': 100,
            'top': 100,
            'width': 200,
            'height': 200,
            'direction': 'down',
            'percent': 0.75
        }
    )
```

#### Exemplo 3: Teste de Permissões

```python
def test_camera_permission(driver):
    """Testa permissão de câmera"""
    
    # Toca botão que requer câmera
    camera_button = driver.find_element(
        AppiumBy.ID,
        'com.example.myapp:id/camera_button'
    )
    camera_button.click()
    
    # Verifica pop-up de permissão
    time.sleep(1)
    
    # Permite (varia por versão Android)
    allow_button = driver.find_element(
        AppiumBy.ID,
        'com.android.permissioncontroller:id/permission_allow_button'
    )
    allow_button.click()
    
    # Valida que câmera abriu
    time.sleep(2)
    camera_preview = driver.find_element(
        AppiumBy.CLASS_NAME,
        'android.view.SurfaceView'
    )
    assert camera_preview.is_displayed()
```

### 4.2 Espresso (Android Nativo)

```java
// LoginActivityTest.java
package com.example.myapp;

import androidx.test.espresso.Espresso;
import androidx.test.espresso.action.ViewActions;
import androidx.test.espresso.assertion.ViewAssertions;
import androidx.test.espresso.matcher.ViewMatchers;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.rule.ActivityTestRule;

import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;

@RunWith(AndroidJUnit4.class)
public class LoginActivityTest {
    
    @Rule
    public ActivityTestRule<LoginActivity> activityRule =
        new ActivityTestRule<>(LoginActivity.class);
    
    @Test
    public void testLoginSuccess() {
        // Digita email
        onView(withId(R.id.email_input))
            .perform(ViewActions.typeText("test@example.com"));
        
        // Digita senha
        onView(withId(R.id.password_input))
            .perform(ViewActions.typeText("password123"));
        
        // Clica botão
        onView(withId(R.id.login_button))
            .perform(ViewActions.click());
        
        // Verifica resultado
        onView(withText("Login Successful"))
            .check(ViewAssertions.matches(
                ViewMatchers.isDisplayed()
            ));
    }
    
    @Test
    public void testEmptyFieldsValidation() {
        onView(withId(R.id.login_button))
            .perform(ViewActions.click());
        
        onView(withText("Please fill all fields"))
            .check(ViewAssertions.matches(
                ViewMatchers.isDisplayed()
            ));
    }
}
```

### 4.3 XCUITest (iOS Nativo)

```swift
// LoginViewControllerUITests.swift
import XCTest

class LoginViewControllerUITests: XCTestCase {
    
    var app: XCUIApplication!
    
    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app = XCUIApplication()
        app.launch()
    }
    
    func testLoginSuccess() {
        // Encontra elementos
        let emailTextField = app.textFields["email_input"]
        let passwordTextField = app.secureTextFields["password_input"]
        let loginButton = app.buttons["login_button"]
        
        // Preenche dados
        emailTextField.tap()
        emailTextField.typeText("test@example.com")
        
        passwordTextField.tap()
        passwordTextField.typeText("password123")
        
        // Clica botão
        loginButton.tap()
        
        // Valida
        let successMessage = app.staticTexts["Login Successful"]
        XCTAssertTrue(successMessage.waitForExistence(timeout: 2))
    }
    
    func testInvalidEmail() {
        let emailTextField = app.textFields["email_input"]
        let loginButton = app.buttons["login_button"]
        
        emailTextField.tap()
        emailTextField.typeText("invalid-email")
        
        loginButton.tap()
        
        let errorMessage = app.staticTexts["Invalid email format"]
        XCTAssertTrue(errorMessage.waitForExistence(timeout: 2))
    }
}
```

---

## 5. Configuração de Device/Emulador

### 5.1 Android Emulator

```bash
# Listar AVDs (Android Virtual Devices)
emulator -list-avds

# Iniciar emulador
emulator -avd MyTestDevice -no-snapshot-save

# Verificar conexão
adb devices

# Instalar app no emulador
adb install app-debug.apk

# Uninstall
adb uninstall com.example.myapp
```

### 5.2 iOS Simulator

```bash
# Listar simuladores
xcrun simctl list devices

# Iniciar simulador
open -a Simulator

# Instalar app
xcrun simctl install booted path/to/app.app

# Uninstall
xcrun simctl uninstall booted com.example.myapp
```

---

## 6. Configuração do Appium Server

### 6.1 Iniciar Manualmente

```bash
# Terminal 1: Iniciar Appium
appium --address 127.0.0.1 --port 4723

# Terminal 2: Rodar testes
pytest tests/test_login.py
```

### 6.2 Programaticamente

```python
from appium.webdriver.appium_service import AppiumService

def setup_module():
    """Setup: Inicia Appium antes dos testes"""
    global service
    service = AppiumService()
    service.start()

def teardown_module():
    """Teardown: Para Appium após os testes"""
    service.stop()
```

---

## 7. Page Object Model (Recomendado)

```python
# pages/base_page.py
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
    
    def find_element(self, locator):
        """Encontra elemento com retry"""
        for _ in range(3):
            try:
                return self.driver.find_element(*locator)
            except:
                time.sleep(0.5)
        raise Exception(f"Elemento não encontrado: {locator}")
    
    def click(self, locator):
        """Clica em elemento"""
        element = self.find_element(locator)
        element.click()
    
    def type_text(self, locator, text):
        """Digita texto"""
        element = self.find_element(locator)
        element.send_keys(text)
    
    def get_text(self, locator):
        """Obtém texto"""
        element = self.find_element(locator)
        return element.text

# pages/login_page.py
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (AppiumBy.ID, 'com.example.myapp:id/email_input')
    PASSWORD_INPUT = (AppiumBy.ID, 'com.example.myapp:id/password_input')
    LOGIN_BUTTON = (AppiumBy.ID, 'com.example.myapp:id/login_button')
    SUCCESS_MSG = (AppiumBy.XPATH, '//*[@text="Login Successful"]')
    ERROR_MSG = (AppiumBy.XPATH, '//*[@text="Invalid credentials"]')
    
    def enter_email(self, email):
        self.type_text(self.EMAIL_INPUT, email)
    
    def enter_password(self, password):
        self.type_text(self.PASSWORD_INPUT, password)
    
    def click_login(self):
        self.click(self.LOGIN_BUTTON)
    
    def is_login_successful(self):
        return self.find_element(self.SUCCESS_MSG).is_displayed()
    
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

# tests/test_login.py
import pytest
from pages.login_page import LoginPage

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

def test_login_success(login_page):
    login_page.login('test@example.com', 'password123')
    assert login_page.is_login_successful()
```

---

## 8. CI/CD para Mobile

### 8.1 GitHub Actions

```yaml
# .github/workflows/mobile-tests.yml
name: Mobile Tests

on: [push, pull_request]

jobs:
  test-android:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Android SDK
      uses: android-actions/setup-android@v2
    
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'
    
    - name: Install Appium
      run: npm install -g appium
    
    - name: Start Emulator
      run: |
        $ANDROID_SDK_ROOT/emulator/emulator -avd TestDevice &
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Run tests
      run: pytest tests/ --html=report.html
    
    - name: Upload report
      if: always()
      uses: actions/upload-artifact@v2
      with:
        name: test-report
        path: report.html

  test-ios:
    runs-on: macos-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Install dependencies
      run: |
        npm install -g appium
        pip install -r requirements.txt
    
    - name: Run tests
      run: pytest tests/ -m ios --html=report.html
    
    - name: Upload report
      if: always()
      uses: actions/upload-artifact@v2
      with:
        name: test-report-ios
        path: report.html
```

### 8.2 Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'npm install -g appium'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Build') {
            steps {
                sh './gradlew build'
            }
        }
        
        stage('Test Android') {
            steps {
                sh 'pytest tests/ -m android --html=report-android.html'
            }
        }
        
        stage('Test iOS') {
            steps {
                sh 'pytest tests/ -m ios --html=report-ios.html'
            }
        }
        
        stage('Report') {
            steps {
                publishHTML([
                    reportDir: '.',
                    reportFiles: 'report-android.html',
                    reportName: 'Android Tests'
                ])
            }
        }
    }
    
    post {
        always {
            junit 'test-results.xml'
        }
    }
}
```

---

## 9. Best Practices

### 9.1 Estrutura de Projeto

```
mobile-tests/
├── tests/
│   ├── test_login.py
│   ├── test_navigation.py
│   └── test_performance.py
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── home_page.py
├── utils/
│   ├── driver_factory.py
│   └── test_data.py
├── config/
│   ├── android_caps.json
│   └── ios_caps.json
├── .github/workflows/
│   └── tests.yml
├── pytest.ini
├── conftest.py
└── requirements.txt
```

### 9.2 conftest.py (Fixtures)

```python
import pytest
from appium import webdriver
import json

@pytest.fixture(scope="session")
def get_caps():
    """Carrega capabilities"""
    platform = pytest.config.option.platform or "android"
    with open(f'config/{platform}_caps.json') as f:
        return json.load(f)

@pytest.fixture
def driver(get_caps):
    """Inicia driver"""
    driver = webdriver.Remote(
        'http://localhost:4723',
        get_caps
    )
    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        help="Platform: android or ios"
    )
```

### 9.3 Waits e Timeouts

```python
from appium.webdriver.support.ui import WebDriverWait
from appium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

def test_with_explicit_wait(driver):
    """Usa espera explícita"""
    wait = WebDriverWait(driver, 10)
    
    # Espera elemento estar visível
    element = wait.until(
        EC.presence_of_element_located((
            AppiumBy.ID,
            'com.example.myapp:id/login_button'
        ))
    )
    element.click()
```

### 9.4 Screenshot e Logs

```python
def test_with_screenshot(driver):
    """Captura screenshot em falhas"""
    try:
        # teste
        pass
    except AssertionError:
        driver.save_screenshot('screenshots/failure.png')
        print(driver.get_log('logcat'))
        raise

@pytest.fixture(autouse=True)
def capture_failure(driver, request):
    """Captura screenshot automaticamente em falhas"""
    yield
    if request.node.rep_call.failed:
        driver.save_screenshot(
            f'screenshots/{request.node.name}.png'
        )
```

### 9.5 Data-Driven Tests

```python
import pytest

test_data = [
    ("test1@example.com", "pass123", True),
    ("test2@example.com", "pass456", True),
    ("invalid@email", "pass", False),
    ("", "pass", False),
]

@pytest.mark.parametrize("email,password,expected", test_data)
def test_login_multiple(driver, email, password, expected):
    """Testa múltiplos dados"""
    login_page = LoginPage(driver)
    login_page.login(email, password)
    
    if expected:
        assert login_page.is_login_successful()
    else:
        assert login_page.is_error_shown()
```

---

## 10. Troubleshooting

| Problema | Solução |
|----------|---------|
| Elemento não encontra | Aumentar timeout, usar diferentes locators |
| Appium timeout | Aumentar `newCommandTimeout` em capabilities |
| Permissões não concedem | Usar `app.grantPermissions()` |
| Emulator não inicia | Checar RAM disponível, criar novo AVD |
| iOS simulator lento | Aumentar alocação de memória |
| Flaky tests | Adicionar waits explícitos, retry logic |

---

## 11. Recursos Adicionais

- **Appium Docs**: http://appium.io/docs
- **Appium Inspector**: Ferramenta visual para encontrar elementos
- **BrowserStack/TestCloud**: Testing cloud for mobile
- **Sauce Labs**: Mobile testing cloud

---

## Conclusão

**Resumo da Estratégia**:
1. Use **Appium** para cross-platform
2. Use **Espresso/XCUITest** para testes nativos rápidos
3. Siga **Page Object Model** para manutenibilidade
4. Implemente **CI/CD** com GitHub Actions ou Jenkins
5. Mantenha **70-80% cobertura** de testes

**Próximas Ações**:
1. Escolher framework (recomendação: Appium)
2. Setup inicial (30 min)
3. Criar primeiros testes (1-2 horas)
4. Integrar CI/CD (2-3 horas)
5. Expandir cobertura (iterativo)
