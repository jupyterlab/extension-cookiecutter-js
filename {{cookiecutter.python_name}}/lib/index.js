module.exports = [
  {
    id: '{{ cookiecutter.labextension_name }}',
    autoStart: true,
    activate: function (app) {
      console.log(
        'JupyterLab extension {{ cookiecutter.labextension_name }} is activated!'
      );
      console.log(app.commands);
    }
  }
];
