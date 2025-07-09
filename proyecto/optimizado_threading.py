from itertools import permutations, combinations
import concurrent.futures
import sys

def disable_gil():
    if sys.version_info >= (3, 13):
        import _thread
        _thread.set_gil_enabled(False)
        print("GIL disabled")
    else:
        print("GIL cannot be disabled in this Python version")



def iteration(num_perm, condition) -> str:
    """"""
    #Disable the GIL for real multithreading
    #disable_gil()


    operadores = ['+', '-', '*', '/']


    for comb in combinations(operadores,4):
        for oper_permu in permutations(comb):

            div_index = {v:k for k,v in dict(enumerate(oper_permu)).items()}["/"]
            if int(num_perm[div_index]) % int(num_perm[div_index + 1]) != 0:
                continue

            expression = num_perm[0] + oper_permu[0] + num_perm[1] + oper_permu[1]  + num_perm[2] + oper_permu[2]  + num_perm[3] + oper_permu[3]  + num_perm[4]
            

            try:
                result = eval(expression)
            except Exception as exc:
                print(f"Generated exception: {exc}, expression: {expression}")
            else:
                #print(f"Expression: {expression}, result: {result}")
                if result.is_integer() and result == condition:
                    #print(f"Expression {expression} found to satisfy the condition {condition}")
                    return expression
                else:
                    return None



def fuerza_bruta_optimizado_threading(condition: int) -> str:

    # Posible combinaciones generadas con la restricciòn
    # de que los nùmeros en el string no pueden repetirse.

    from itertools import permutations, combinations
    import ast

    numeros = range(1, 10)
    res_expression = None

    # Lista para almacenar permutaciones completas
    permutaciones_completas = []

    # Paso 1: combinar 5 números únicos con los 4 operadores
    for seleccion_numeros in combinations(numeros, 5):
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                # Start the load operations and mark each future with its URL
                future_perm = {executor.submit(iteration, "".join([str(e) for e in list(perm)]), condition): "".join([str(e) for e in list(perm)]) for perm in permutations(seleccion_numeros)}
                for future in concurrent.futures.as_completed(future_perm):
                    selection = future_perm[future]
                    try:
                        res_expression = future.result()
                        if res_expression is not None:
                            break

                    except Exception as exc:
                        print('%r generated an exception: %s' % (selection, exc))
                    else:
                        print(f"Thread completed: {future}")
                 
    print(f"Expression {res_expression} found to satisfy the condition {condition}")
    return res_expression              
                
if __name__ == "__main__":
    """"""
    fuerza_bruta_optimizado_threading(100)