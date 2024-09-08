def teste (valor):
    print(valor)
    
cond1 = 2    
    
teste("CONDIÇÃO FALSA" if not cond1 
      else "FALTOU" if cond1 == 1 
      else "ATESTADO" if cond1 == 2
      else 0)
