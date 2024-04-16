from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from organizer.Organiser import OrganiseByType  # Assuming the function to organize files is called 'organize_files'

class OrganizerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.working_dir_label = Label(text='Enter the folder to be organized:')
        self.working_dir_input = TextInput(multiline=False)
        self.dst_dir_label = Label(text='Enter the folder that the organized files will be copied:')
        self.dst_dir_input = TextInput(multiline=False)

        self.organize_button = Button(text='Organize')
        self.organize_button.bind(on_press=self.organize)

        layout.add_widget(self.working_dir_label)
        layout.add_widget(self.working_dir_input)
        layout.add_widget(self.dst_dir_label)
        layout.add_widget(self.dst_dir_input)
        layout.add_widget(self.organize_button)

        return layout

    def organize(self, instance):
        working_dir = self.working_dir_input.text
        dst_dir = self.dst_dir_input.text
        organize_files(working_dir, dst_dir)  # Call the function to organize files

if __name__ == '__main__':
    OrganizerApp().run()