Feature: login de usuario

  Scenario: login realizado com sucesso
     Given que o usuario insira e-mail e senha corretos
      When ele tenta logar no sistema
      Then sistema apresenta a tela inicial