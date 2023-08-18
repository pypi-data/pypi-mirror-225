from flask import render_template, redirect, url_for

class CLASSNAME:

    def index(self):  
        return render_template('NAME/index.html')

    def read(self, id):
        return render_template('NAME/view.html')

    def get_store(self):
        return render_template('NAME/store.html')
    
    def post_store(self):
        return redirect(url_for('NAME_index'))

    def get_update(self, id):
        return render_template('NAME/update.html')
    
    def post_update(self, id):
        return redirect(url_for('NAME_view', id=id))

    def delete(self, id):
        return redirect(url_for('NAME_index'))

