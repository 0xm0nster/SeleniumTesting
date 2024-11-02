from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

class MySeleniumTests(StaticLiveServerTestCase):
	# no crearem una BD de test en aquesta ocasió (comentem la línia)
	#fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()
    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()
 
    def test(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
 
        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )
 
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
 
        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )
        self.selenium.find_element(By.XPATH,'/html/body/div/div/main/div/div[1]/div[1]/table/tbody/tr[2]/td[1]/a').click()
        #Creem el nou Usuari
        username_camp = self.selenium.find_element(By.XPATH,'//*[@id="id_username"]')
        username_camp.send_keys('isardstaff')
        password_camp = self.selenium.find_element(By.XPATH,'//*[@id="id_password1"]')
        password_camp.send_keys('contrasenyastaff')
        passwordv_camp = self.selenium.find_element(By.XPATH,'//*[@id="id_password2"]')
        passwordv_camp.send_keys('contrasenyastaff')
        self.selenium.find_element(By.XPATH,'/html/body/div/div/main/div/div/form/div/div/input[1]').click()
        self.selenium.find_element(By.XPATH,'//*[@id="id_is_staff"]').click()
        camp_permisos = self.selenium.find_element(By.XPATH,'//*[@id="id_user_permissions_input"]')
        #Afegim permisos al usuari
        camp_permisos.send_keys('Authentication and authorization can add user',Keys.RETURN)
        camp_permisos.send_keys('Authentication and authorization can change user',Keys.RETURN)
        camp_permisos.send_keys('Authentication and authorization can view user',Keys.RETURN)
        self.selenium.find_element(By.XPATH,'/html/body/div[1]/div/main/div/div/form/div/div/input[1]').click()
        self.selenium.find_element(By.XPATH,'/html/body/div[1]/header/div[2]/form/button').click()
        self.selenium.find_element(By.XPATH,'/html/body/div/div/main/div/p[2]/a').click()
        #Loguejem com el nou usuari i testejem permisos
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isardstaff')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('contrasenyastaff')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
        try:
            crear_user = self.selenium.find_element(By.CLASS_NAME, 'addlink')
            self.assertTrue(crear_user.is_displayed(), "No s'ha trobat addlink")
        except NoSuchElementException:
            self.fail("No s'ha trobat addlink, test fallat sense excepció.")
        questions_element = self.selenium.find_elements(By.XPATH, "//*[contains(text(), 'Questions')]")
        self.assertEqual(len(questions_element), 0, "S'ha trobat Questions")
        
		
