import cmdOptions.Controller as c

class Test_AutoController:

    controller = c.Controller()

    def option1_test():
            print("option1")

    def option2_test():
        print("option2")

    def test_add_option(self):

        self.controller.addOption("option1", Test_AutoController.option1_test)
        self.controller.addOption("option2", Test_AutoController.option2_test)

        assert self.controller.get_options() == ["option1", "option2"]

    def test_add_list_length(self):

        assert self.controller.get_optionListLength() == 2
    
    def test_remove_option(self):
        
        self.controller.removeOption("option1")

        assert self.controller.get_options() == ["option2"]

    def test_remove_list_length(self):
         assert self.controller.get_optionListLength() == 1
        

    def test_clear_options(self):
        self.controller.clearOptions()

        assert self.controller.get_optionListLength() == 0