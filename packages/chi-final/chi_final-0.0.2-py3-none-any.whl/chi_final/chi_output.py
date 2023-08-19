from chi_bhargab_2 import chi_performance, chi_performance_parsed_table
class feed_data:
  def __init__(self, data, percentage, column1, column2, column3):
    self.df=data
    self.percentage=percentage
    self.column1=column1
    self.column2=column2
    self.column3=column3
    abraca_dabra=chi_performance.test(self.df,self.column1, self.column2, self.column3)
    a,b=abraca_dabra.result()
    w=chi_performance_parsed_table.data_feed(self.percentage,self.df,a,b,self.column1, self.column2, self.column3)
  def interpret(self):
    intprt=w.interpret()
    return intprt
  def op_table(self):
    op_table=w.output_table()
    return op_table