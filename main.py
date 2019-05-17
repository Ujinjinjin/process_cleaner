try:
    if __name__ == '__main__':
        from program.program import Program

        program: Program = Program(main_file=__file__, settings_filename='settings.json')
        program.start()

except Exception as ex:
    print(ex)
    input('Press enter to continue')
