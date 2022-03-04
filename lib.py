from menu import Menu


class Lib:

    @staticmethod
    def app_header():
        Menu.clear()
        Menu.hbar()
        Menu.htext()
        Menu.htext('FCC 477 Submission Preparation Tool')
        Menu.htext('By Azorian Solutions')
        Menu.htext()
        Menu.htext('https://azorian.solutions')
        Menu.htext()
        Menu.htext('Copyright (c) 2022 Azorian Solutions LLC.')
        Menu.htext()
        Menu.hbar()

    @staticmethod
    def bd_header():
        Lib.app_header()
        Menu.text()
        Menu.text('Broadband Deployment Mode', align='center')
        Menu.text()
        Menu.hbar()

    @staticmethod
    def bs_header():
        Lib.app_header()
        Menu.text()
        Menu.text('Broadband Subscription Mode', align='center')
        Menu.text()
        Menu.hbar()

    @staticmethod
    def api_key_warning():
        Lib.app_header()
        Menu.text()
        Menu.text()
        Menu.text('No Geocod.io API key has been provided but one is required to use bs mode!', align='center')
        Menu.text()
        Menu.text('Please specify an API key with the -k (--apikey) parameter.', align='center')
        Menu.text()
        Menu.text('You may obtain an API key here: https://dash.geocod.io/apikey', align='center')
        Menu.text()
        Menu.text()
        Menu.hbar()

    @staticmethod
    def bd_consumer_service(msg=None):
        Lib.bd_header()
        Menu.text()
        Menu.text()
        Menu.text('Do all the provided census blocks offer mass market / consumer broadband service?', align='center')
        Menu.text()

        if msg is not None:
            Menu.text(msg)
            Menu.text()

        answer = Menu.collect_input('Your answer [yes or no]: ')

        if answer not in ('yes', 'y', '1', 'no', 'n', '0'):
            return Lib.bd_consumer_service('The answer given of "' + answer + '" is not valid. Please try again.')

        if answer in ('yes', 'y', '1'):
            return '1'
        else:
            return '0'

    @staticmethod
    def bd_business_service(msg=None):
        Lib.bd_header()
        Menu.text()
        Menu.text()
        Menu.text('Do all the provided census blocks offer business / government broadband service?', align='center')
        Menu.text()

        if msg is not None:
            Menu.text(msg)
            Menu.text()

        answer = Menu.collect_input('Your answer [yes or no]: ')

        if answer not in ('yes', 'y', '1', 'no', 'n', '0'):
            return Lib.bd_consumer_service('The answer given of "' + answer + '" is not valid. Please try again.')

        if answer in ('yes', 'y', '1'):
            return '1'
        else:
            return '0'

    @staticmethod
    def bd_advertised_downstream(msg=None):
        Lib.bd_header()
        Menu.text()
        Menu.text()
        Menu.text('For consumer plans, what is the maximum downstream bandwidth (in Mbps) that you offer in all '
                  + 'provided census blocks?', align='center')
        Menu.text()
        Menu.text('For mass market / consumer broadband services, the maximum advertised downstream bandwidth available'
                  + ' in the census block in Mbps. If bandwidths are not advertised, enter the highest downstream '
                  + 'bandwidth an end user in the block can reasonably expect to receive over the technology. You can '
                  + 'enter up to 3 places after the decimal (e.g., 768 kbps would be entered as 0.768). If you answered'
                  + ' yes to the first question (“Consumer”), there should be a non-zero value in this field.')
        Menu.text()

        if msg is not None:
            Menu.text(msg)
            Menu.text()

        answer = round(float(Menu.collect_input('Your answer [Mbps]: ')), 0)

        if answer < 1:
            return Lib.bd_consumer_service('The answer given of "' + answer + '" is not valid. You must specify at '
                                           + 'least 1 Mbps.')

        return answer

    @staticmethod
    def bd_advertised_upstream(msg=None):
        Lib.bd_header()
        Menu.text()
        Menu.text()
        Menu.text('For consumer plans, what is the maximum upstream bandwidth (in Mbps) that you offer in all provided'
                  + ' census blocks?', align='center')
        Menu.text()
        Menu.text('For mass market / consumer broadband services, the maximum advertised upstream bandwidth that is '
                  + 'offered with the above maximum advertised downstream bandwidth available in the census block in '
                  + 'Mbps. If bandwidths are not advertised, enter the highest upstream bandwidth an end user in the '
                  + 'block can reasonably expect to receive, in a service option with the above downstream bandwidth, '
                  + 'over the technology. You can enter up to 3 places after the decimal (e.g., 768 kbps would be '
                  + 'entered as 0.768). If you answered yes to the first question, there should be a non-zero value in '
                  + 'this field.')
        Menu.text()

        if msg is not None:
            Menu.text(msg)
            Menu.text()

        answer = round(float(Menu.collect_input('Your answer [Mbps]: ')), 0)

        if answer < 1:
            return Lib.bd_consumer_service('The answer given of "' + answer + '" is not valid. You must specify at '
                                           + 'least 1 Mbps.')

        return answer

    @staticmethod
    def bd_status_msg(msg=None, header=False, footer=False, buffer=True, align='left'):
        if header:
            Lib.bd_header()
        if buffer:
            Menu.text()
        Menu.text(msg, align=align)
        if buffer:
            Menu.text()
        if footer:
            Menu.hbar()

    @staticmethod
    def bs_status_msg(msg=None, header=False, footer=False, buffer=True, align='left'):
        if header:
            Lib.bs_header()
        if buffer:
            Menu.text()
        Menu.text(msg, align=align)
        if buffer:
            Menu.text()
        if footer:
            Menu.hbar()

    @staticmethod
    def bs_create_plan_id(row):
        plan_id = ''

        if 'ds' in row and row['ds'] > 0:
            plan_id += str(row['ds'])
            if 'dsu' in row and len(row['dsu']):
                plan_id += row['dsu']

        if 'us' in row and row['us'] > 0:
            if len(plan_id):
                plan_id += 'x'
            plan_id += str(row['us'])
            if 'usu' in row and len(row['usu']):
                plan_id += row['usu']

        return plan_id
