using Additive_Translator.misc;

namespace Additive_Translator
{
    public class FilesHistory
    {
        public List<ParseStateModel> History { get; }

        public FilesHistory()
        {
            History = new List<ParseStateModel>();
        }
    }
}
