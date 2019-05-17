try:
    if __name__ == '__main__':
        from program.program import Program

        program: Program = Program(__file__)
        program.start()

except Exception as ex:
    print(ex)
    input('Press enter to continue')
