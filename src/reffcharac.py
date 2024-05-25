
import sys

# nmos
# {model_type}_{model_name} d_{model_name} g_{model_name} s_{model_name} b_{model_name} {model_name} L={length} W={width}
# v_d_{model_name} d_{model_name} 0 dc 0.0
# v_g_{model_name} d_{model_name} 0 dc {vdd}
# v_s_{model_name} d_{model_name} 0 dc 0.0
# v_b_{model_name} d_{model_name} 0 dc 0.0
# .measure {model_name}_start find i(v_d_{model_name}) at = 0.0
# .measure {model_name}_end   find i(v_d_{model_name}) at = 0.01
# .measure {model_name}_reff  param = '({model_name}_end-model_name}_start)/(0.01)'
# pmos
# {model_type}_{model_name} d_{model_name} g_{model_name} s_{model_name} b_{model_name} {model_name} L={length} W={width}
# v_d_{model_name} d_{model_name} 0 dc {vdd}
# v_g_{model_name} d_{model_name} 0 dc 0.0
# v_s_{model_name} d_{model_name} 0 dc {vdd}
# v_b_{model_name} d_{model_name} 0 dc {vdd}
# .measure {model_name}_start find i(v_d_{model_name}) at = {vdd}
# .measure {model_name}_end   find i(v_d_{model_name}) at = '{vdd}-0.01'
# .measure {model_name}_reff  param = '({model_name}_end-model_name}_start)/(0.01)'

class Model:
    def __init__(self, model_name = 'nmos', length=1.0, width=1.0, vdd=1.0, subckt_model='m', model_type='n'):
        self.m_model_name       = model_name
        self.m_length           = length        # um
        self.m_width            = width         # um
        self.m_vdd              = vdd           # vdd voltage
        self.m_subckt_model     = subckt_model  # 'm' : mosfet, 'x' : subckt
        self.m_model_type       = model_type    # 'n' : nmos,   'p' : pmos 
        self.m_reff             = 1.0           # Ohm
    def SetModelName(self, model_name):
        self.m_model_name       = model_name
    def GetModelName(self):
        return self.m_model_name
    def SetLength(self, length):
        self.m_length           = length
    def GetLength(self):
        return self.m_length
    def SetWidth(self, width):
        self.m_width            = width
    def GetWidth(self):
        return self.m_width
    def SetSubcktModel(self, subckt_model):
        self.m_subckt_model     = subckt_model
    def GetSubcktModel(self):
        return self.m_subckt_model
    def SetModelType(self, model_type):
        self.m_mode_type        = model_type
    def GetModelType(self):
        return self.m_model_type
    def SetVdd(self, vdd):
        self.m_vdd              = vdd
    def GetVdd(self):
        return self.m_vdd
    def SetReff(self, reff):
        self.m_reff = reff
    def GetReff(self):
        return self.m_reff
    def GetInfoStr(self):
        return f'{self.GetModelName()} {self.GetLength()} {self.GetWidth()} {self.GetSubcktModel()} {self.GetModelType()} {self.GetVdd()} {self.GetReff()}'
        
class ReffCharac:
    def __init__(self):
        self.m_input_filename   = ''
        self.m_output_prefix    = ''
        self.m_inc_filename     = ''
        self.m_models           = {}                # key : model_name, data : model
#        self.m_spice_filename   = ''
#        self.m_measure_filename = ''
    def SetInputFilename(self, input_filename):
        self.m_input_filename = input_filename
    def GetInputFilename(self):
        return self.m_input_filename
    def SetOutputPrefix(self, output_prefix):
        self.m_output_prefix = output_prefix
    def GetOutputPrefix(self):
        return self.m_output_prefix
    def SetIncFilename(self, inc_filename):
        self.m_inc_filename = inc_filename
    def GetIncFilename(self):
        return self.m_inc_filename
    def PrintUsage(self):
        print(f'reff_charac.py usage:')
        print(f'% python3 reff_charac.py input_file output_prefix inc_file')
    def Run(self, args):
        print(f'# reff_charac.py start')
        if 4 != len(args):
            self.PrintUsage()
            exit()
        self.ReadArgs(args)
        self.ReadInputFile()
        self.MakeSpiceInputDeck()
        self.PrintModels()
        print(f'# reff_charac.py end')
    def ReadArgs(self, args):
        print(f'# read args start')
        self.SetInputFilename(args[1])
        self.SetOutputPrefix(args[2])
        self.SetIncFilename(args[3])
        #
#        self.m_spice_filename   = self.GetOutputPrefix() + '.reff.sp'
#        self.m_measure_filename = self.GetOutputPrefix() + '.reff.meas'
        print(f'# read args end')
    # input file format
    # model_name length[um] width[um] vdd[V] subckt_model(x or m) model_type(n or p)
    def ReadInputFile(self):
        print(f'# read input file({self.GetInputFilename()}) start')
        input_file = open(self.GetInputFilename(), 'rt')
        while True:
            line = input_file.readline()
            if not line:
                break
            line = line.lstrip().rstrip()
            if '*' == line[0]:
                continue
            tokens  = line.split()
            if 6 != len(tokens):
                continue
            model_name      = tokens[0] 
            if not model_name in self.m_models:
                length          = float(tokens[1])
                width           = float(tokens[2])
                vdd             = float(tokens[3])
                subckt_model    = tokens[4]
                model_type      = tokens[5]
                model           = Model(model_name, length, width, vdd, subckt_model, model_type)
                self.m_models[model_name]   = model
        print(f'# read input file({self.GetInputFilename()}) end')
    def PrintModels(self):
        print(f'# print models start')
        for model_name in self.m_models:
            model = self.m_models[model_name]
            print(f'{model.GetInfoStr()}')
        print(f'# print models end')
    def MakeSpiceInputNetlist(self, spice_file, model):
        name    = f'{model.GetSubcktModel()}_{model.GetModelName()}'
        d       = f'd'
        g       = f'g_{model.GetModelName()}'
        s       = f's_{model.GetModelName()}'
        b       = f'b_{model.GetModelName()}'
        prop    = f'{model.GetModelName()} L={model.GetLength()} W={model.GetWidth()}'
        #
        spice_file.write(f'{name} d {g} {s} {b} {prop}\n')
        #
        if 'n' == model.GetModelType():
#            spice_file.write(f'v_d d 0 dc 0.0\n')
            spice_file.write(f'v_{g} {g} 0 dc {model.GetVdd()}\n')
            spice_file.write(f'v_{s} {s} 0 dc 0.0\n')
            spice_file.write(f'v_{b} {b} 0 dc 0.0\n')
            spice_file.write(f'.measure dc {model.GetModelName()}_start find i(v_{d}) at = 0.0\n')
            spice_file.write(f'.measure dc {model.GetModelName()}_end   find i(v_{d}) at = 0.01\n')
            spice_file.write(f'.measure dc {model.GetModelName()}_reff  param=\'({model.GetModelName()}_end - {model.GetModelName()}_start)/(0.01)\'\n')
        elif 'p' == model.GetModelType():
#            spice_file.write(f'v_d d 0 dc {model.GetVdd()}\n')
            spice_file.write(f'v_{g} {g} 0 dc 0.0\n')
            spice_file.write(f'v_{s} {s} 0 dc {model.GetVdd()}\n')
            spice_file.write(f'v_{b} {b} 0 dc {model.GetVdd()}\n')
            spice_file.write(f'.measure dc {model.GetModelName()}_start find i(v_{d}) at = {model.GetVdd()}\n')
            spice_file.write(f'.measure dc {model.GetModelName()}_end   find i(v_{d}) at = {model.GetVdd() - 0.01}\n')
            spice_file.write(f'.measure dc {model.GetModelName()}_reff  param=\'({model.GetModelName()}_end - {model.GetModelName()}_start)/(0.01)\'\n')
    def MakeSpiceInputDeck(self):
        print(f'# make spice input deck file start')
        spice_file      = open(self.m_spice_filename, 'wt')
        #
        spice_file = open(self.m_spice_filename, 'wt')
        spice_file.write(f'# reff charac.\n')
        spice_file.write(f'.inc \"{self.m_inc_filename}\"\n')
        spice_file.write(f'.option scale=1u\n')
        spice_file.write(f'v_d d 0 dc 0.0\n')
        #
        for model_name in self.m_models:
            model       = self.m_models[model_name]
            self.MakeSpiceInputNetlist(spice_file, model)
        #
        vdd_max     = self.GetMaxVdd()
        spice_file.write(f'.dc v_d 0.0 {vdd_max} 0.01\n')
        spice_file.write('.end\n')
        spice_file.close()
        print(f'# make spice input deck file end')
    def RunSpice(self):
        print(f'# run spice start')
        print(f'# run spice end')
    def ReadMeasureFile(self):
        print(f'# read measure file({self.m_measure_filename}) start')
        measure_file    = open(self.m_measure_filename, 'rt')
        measure_file.close()
        print(f'# read measure file({self.m_measure_filename}) end')
    def GetMaxVdd(self):
        max_vdd     = -sys.float_info.max
        for model_name in self.m_models:
            model = self.m_models[model_name]
            if max_vdd <= model.GetVdd():
                max_vdd = model.GetVdd()
        return max_vdd
        
def main(args):
    reff_charac     = ReffCharac()
    reff_charac.Run(args)
    
if __name__ == '__main__':
    main(sys.argv)