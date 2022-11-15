import fpdf 
from datetime import datetime
from pathlib import Path






class PDF(fpdf.FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        self.SIDE_MARGIN = 10
        self.PADDING = 5

        self.FIRST_COLUMN_X = self.SIDE_MARGIN
        self.COLUMN_WIDTH = self.WIDTH / 2 - self.SIDE_MARGIN - self.PADDING
        self.SECOND_COLUMN_X = self.WIDTH / 2 + self.PADDING
        self.ASSETS = Path(__file__).parent / "assets"



    def header(self):
        # Custom logo and positioning
        # Create an `assets` folder and put any wide and short image inside
        # Name the image `logo.png`
        self.image(str(self.ASSETS / 'logo.png'), 10, 8, 33)
        self.set_font('Times', 'B', 11)
        self.cell(self.WIDTH - 80)
        self.ln(20)
        
    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def frontpage(self, last_report_date, today_date):

        self.add_page()
        self.set_font('Times', 'B', 48)
        self.cell(0, 100, 'Steintest report', 0, 0, 'C')
        self.set_font('Times', 'B', 16)
        self.ln(20)
        self.cell(0, 100, last_report_date.strftime("%m/%d/%Y") + " - " + today_date.strftime("%m/%d/%Y"), align='C')
        #self.image(str(self.ASSETS / 'frontpage-picture.png'), self.WIDTH / 2 - 70, self.HEIGHT / 2 - 40, 140)

    def quick_overview(self, num_tests_since_last_report, deviation_in_num_tests, nums_of_test_singapore, nums_of_test_new_york, nums_of_test_amsterdam, PLOT_FOLDER_PATH):
        self.add_page()
        self.set_font('Times', 'B', 16)
        self.cell(0, 10, 'Quick overview', 0, 0, 'C')
        self.ln(20)
        self.set_font('Times', '', 12)
        self.cell(80, 10, 'Number of tests since last report:', 0, 0, 'L')
        self.cell(100, 10, str(num_tests_since_last_report), 0, 1, 'L')

        self.cell(80, 10, "Change compared to last report:", 0, 0, 'L')
        self.cell(100, 10, str(deviation_in_num_tests), 0, 1, 'L')
        self.ln(10)
        self.cell(80, 10, "Number of tests per server:", 0, 1, 'L')

        self.set_x(20)
        self.multi_cell(80, 10, f"Amsterdam:  {str(nums_of_test_amsterdam)}\nNew York:  {str(nums_of_test_new_york)}\nSingapore:  {str(nums_of_test_singapore)}", 
                                    0, 0, 'L')

                
        self.image(str(PLOT_FOLDER_PATH / "tests_over_time_per_server.png"), self.SECOND_COLUMN_X, 40, self.COLUMN_WIDTH)
        
        self.image(str(PLOT_FOLDER_PATH / "tests_over_time.png"), self.SECOND_COLUMN_X, 120, self.COLUMN_WIDTH)

        

    def geographical_coverage(self, PLOT_FOLDER_PATH):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Geographical coverage', 0, 0, 'C')
 
        self.ln(20)
    
        self.set_font('Times', '', 12)


        ## Insert text here
        self.multi_cell(
            w=self.COLUMN_WIDTH,
            h=10,
            txt= "This section will cover how geographical location impacts a connection"
        )
        

        self.image(str(PLOT_FOLDER_PATH / "box_plots_of_packetloss_per_continent.png"), self.SECOND_COLUMN_X, 40, self.COLUMN_WIDTH)
        
        self.image(str(PLOT_FOLDER_PATH / "scatter_plot_of_distance_to_server_and_packetloss.png"), self.SECOND_COLUMN_X, 120, self.COLUMN_WIDTH)

        self.image(str(PLOT_FOLDER_PATH / "tests_over_time_per_continent.png"), self.SECOND_COLUMN_X, 200, self.COLUMN_WIDTH)

    def all_time_overview(self, PLOT_FOLDER_PATH):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'All time overview', 0, 0, 'C')



        
        
        self.add_page()
        self.image(str(PLOT_FOLDER_PATH / "cdf_over_number_of_lost_packets.png"), self.FIRST_COLUMN_X, 20, self.COLUMN_WIDTH)

    def os_and_browser_section(self, PLOT_FOLDER_PATH):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'OS and Browser investigation', 0, 0, 'C')
        self.ln(20)

        self.set_font('Times', '', 12)
        ## Insert text here
        self.multi_cell(
            w=self.COLUMN_WIDTH,
            h=10,
            txt= "This section will cover how os and browser impacts a connection"
        )

        self.image(str(PLOT_FOLDER_PATH / "box_plots_over_OS.png"), self.SECOND_COLUMN_X, 40, self.COLUMN_WIDTH)

    def burstyness_section(self, PLOT_FOLDER_PATH):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Investigation of bursty peacketloss', 0, 0, 'C')
        self.ln(20)

        self.set_font('Times', '', 12)
        ## Insert text here
        self.multi_cell(
            w=self.COLUMN_WIDTH,
            h=10,
            txt= "This section will cover how bursty packetloss impacts a connection"
        )

        self.image(str(PLOT_FOLDER_PATH / "consecutive_lost_packets_histogram.png"), self.FIRST_COLUMN_X, None, self.COLUMN_WIDTH)

    def general_plots(self, PLOT_FOLDER_PATH):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'General plots', 0, 0, 'C')

        self.image(str(PLOT_FOLDER_PATH / "scatter_plot_of_packetloss_and_latency.png"), self.SECOND_COLUMN_X, 40, self.COLUMN_WIDTH)

        self.image(str(PLOT_FOLDER_PATH / "scatter_plot_of_speed_and_packetloss.png"), self.SECOND_COLUMN_X, 120, self.COLUMN_WIDTH)

        self.image(str(PLOT_FOLDER_PATH / "cdf_over_number_of_lost_packets.png"), self.SECOND_COLUMN_X, 200, self.COLUMN_WIDTH)

    def stat_section(self, PLOT_FOLDER_PATH):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'The Statistical investigation of the data', 0, 0, 'C')


    def Appendix(self):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Appendix', 0, 0, 'C')
        self.ln(20)

