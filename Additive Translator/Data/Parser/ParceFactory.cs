using System;
using System.IO;
using Additive_Translator.Data.Interfaces;
using Additive_Translator.Data.Models;
using Additive_Translator.Data.Parser.Convertors;

namespace Additive_Translator.Data.Convertor
{
    public class ParceFactory: IParserFactory
    {
        public void Parce(ParceReqestModel inputParceReqestModel)
        {
            ITranslator translator;
            if (inputParceReqestModel.TargetRobot == Enums.RobotTargetEnum.Fanuc)
            {
                translator = Path.GetExtension(inputParceReqestModel.InputFilePath) switch
                {
                    ".gcode" => new ConverterGcode(inputParceReqestModel),
                    ".lsr" => new ConverterPowerMill(inputParceReqestModel),
                    _ => throw new FormatException("Source file with such extension is not supported")
                };
            }
            else
            {
                translator = new KukaTranslatorProvider(inputParceReqestModel);
            }
            
            translator.Process();
        }
    }
}