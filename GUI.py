import PySimpleGUI as sg
from Retire_Calc import retire
from helpers import draw_figure



HEIGHT = 700
WIDTH = 1000


# FrontEnd
input_layout = [

    [sg.Text("Enter Age"), sg.InputText(key = "AGE", size = (10, 1))],
    #[sg.Text("Select Race (Selection must turn box black)"), sg.Combo(['White', 'Black', 'Hispanic', 'Native American', 'Alaskan/Pacific Islander'], key = "RACE", default_value='White', readonly=True)],
    [sg.Text("Enter Gender"), sg.Combo(['Male', 'Female'], key = "GENDER", default_value='Male')],
    [sg.Text("Enter Desired Retirement Year"), sg.InputText(key = "RETIREMENT_YEAR", size = (10,1))],
    [sg.Text("How much are your current assets worth? (Real Estate, Cash, Savings, Annuities)"), sg.InputText(key = "CASH", size = (10, 1))],
    [sg.Text("How much do you currently have invested in stocks?"), sg.InputText(key = "STOCKS", size = (10, 1))],
    [sg.Text("How much do you have currently invested in bonds or other fixed-income assets?"), sg.InputText(key = "BONDS", size = (10, 1))],
    #[sg.Text("How much money would you like to live off of per year in retirement?"), sg.InputText(key = "GOAL", size = (10, 1))],
    #[sg.Text("How much money are you currently making per year, before savings and retirement?"), sg.InputText(key = "INCOME", size = (10, 1))],
    [sg.Submit(), sg.Exit()]

]


output_layout = [
    [sg.Column([
        [sg.Frame(title = "Input Life Expentancy Information", layout = [
            [sg.Text("Age: "), sg.Text(size = (15, 1), key = '-AGE_OUT-', text_color = 'yellow')],
            #[sg.Text("Race: "), sg.Text(size = (15, 1), key = '-RACE_OUT-', text_color = 'yellow')],
            [sg.Text("Gender: "), sg.Text(size = (15, 1), key = '-GENDER_OUT-', text_color = 'yellow')],
            ]
        )],
        [sg.Frame(title = "Output Life Expentancy Information", layout = [
            [sg.Text("Life Expentancy: "), sg.Text(size = (15, 1), key = '-DEATH_AGE-', text_color = 'yellow')],
            #[sg.Text("% Chance of Dying this Year: "), sg.Text(size = (15, 1), key = '-DEATH_PERC-', text_color = 'yellow')],
            [sg.Text("Probable Years Left Alive: "), sg.Text(size = (15, 1), key = '-DEATH_YEARS-', text_color = 'yellow')],
            ]
        )],
        [sg.Frame(title = "Chance of Death vs. Age", size = (WIDTH * .4, HEIGHT * .7), layout = [
            [sg.Canvas(key = "-DEATH_PLOT-")]
            ]
        )]
    ], size= (WIDTH * .4, HEIGHT)),

    sg.Column([
        [sg.Frame(title = "Output Retirement Information", layout = [
            [sg.Text("Life Expentancy Post-Retirement: "), sg.Text(size = (15, 1), key = '-POST_RET-', text_color = 'yellow')],
            [sg.Text("Years Until Retirement: "), sg.Text(size = (15, 1), key = '-TILL_RETIRE-', text_color = 'yellow')],
            [sg.Text("Retirement Year: "), sg.Text(size = (15, 1), key = '-RETIRE_YEAR-', text_color = 'yellow')]
            ]
        )],
        [sg.Frame(title = "Current Distribution of Assets vs Ideal Distribution", size = (WIDTH * .6, HEIGHT * .3), layout = [
            [sg.Canvas(key = "-ASSET_DISTRIBUTION-")]
            ]
        )],
        [sg.Frame(title = "Retirement Glideslope", size = (WIDTH * .6, HEIGHT * .60), layout = [
            [sg.Canvas(key = "-GLIDESLOPE-")]
            ]
        )]
    ], size= (WIDTH * .6, HEIGHT))
]]














# Backend




input_window = sg.Window("RoboAdvisor", input_layout)
while True:
    input_event, input_values = input_window.read()
    #print(event, values)

    run_calc = False

    if input_event in (sg.WINDOW_CLOSED, "Exit"):
        break

    if input_event == "Submit":

        print(input_values)

        if "" in input_values.values():
            sg.popup_error("Please enter a value in all boxes")

        else:
            client = retire(input_values['AGE'], input_values['RETIREMENT_YEAR'], input_values['CASH'], input_values['STOCKS'], input_values['BONDS'], input_values['GENDER'])
            value_check = client.check_values()

            if value_check != True:
                sg.popup_error(value_check)

            else:
                run_calc = True
            


    if run_calc == True:
        input_window.close()
        output_window = sg.Window("RoboAdvisor", output_layout, size = (WIDTH, HEIGHT), finalize = True)

        while True:
            

            death_age, death_perc, death_years, death_figure = client.calc_death()
            years_after_retirement, years_till_retirement, dist_figure, glideslope = client.retire_calc()




            output_window["-AGE_OUT-"].update(str(client.age))
            #output_window["-RACE_OUT-"].update(str(client.race))
            output_window["-GENDER_OUT-"].update(str(client.gender))
            output_window["-DEATH_AGE-"].update(str(death_age))
            #output_window["-DEATH_PERC-"].update(str(death_perc))
            output_window["-DEATH_YEARS-"].update(str(death_years))

            # output_window["-EQ_OUT-"].update(str(client.stocks))
            # output_window["-FIXED_OUT-"].update(str(client.bonds))
            # output_window["-CASH_OUT-"].update(str(client.cash))

            output_window["-POST_RET-"].update(str(years_after_retirement))
            output_window["-RETIRE_YEAR-"].update(str(client.retirement_year))
            output_window["-TILL_RETIRE-"].update(str(years_till_retirement))
    


            
            fig_canvas_agg =  draw_figure(output_window['-DEATH_PLOT-'].TKCanvas, death_figure)
            fig_canvas_agg =  draw_figure(output_window['-ASSET_DISTRIBUTION-'].TKCanvas, dist_figure)
            fig_canvas_agg =  draw_figure(output_window['-GLIDESLOPE-'].TKCanvas, glideslope)


            event, values = output_window.read()


            if event in (sg.WINDOW_CLOSED, "Exit"):
                break
                

