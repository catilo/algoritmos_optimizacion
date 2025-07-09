from itertools import product, combinations_with_replacement
import concurrent.futures
import sys 

if __name__ == "__main__":
    

    numeros = range(1, 10)
    operadores = ['+', '-', '*', '/']

    # Lista para almacenar permutaciones completas
    counter = 0


    def calcPermutations(seleccion_numeros,operadores):
        """"""
        count = 0
        elementos = list(seleccion_numeros) + operadores  # total 9 elementos
        for perm in product(elementos, repeat=9):
            count += 1

        return count

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Start the load operations and mark each future with its URL
        future_perm = {executor.submit(calcPermutations, seleccion_numeros,operadores): str(seleccion_numeros) for seleccion_numeros in combinations_with_replacement(numeros, 5)}
        for future in concurrent.futures.as_completed(future_perm):
            selection = future_perm[future]
            try:
                count = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (selection, exc))
            else:
                print('%r page is %d count ' % (selection, count))
                counter += count
                print( f"counter:  {counter}")

    print(f"Counter: {counter}")