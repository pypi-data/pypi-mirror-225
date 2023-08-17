import json

class File:

    @staticmethod
    def readJsonFile(filePath:str, encoding:str="utf-8"):
        """
        filePath: 文件路径
        encoding:文件编码
        return     json 对象
        """
        with open(filePath, "r", encoding=encoding) as f:
            result = json.load(f) 
            return result
    
    @staticmethod
    def writeJsonFile(filePath,obj):
        """
        filePath: 文件路径
        obj : 待写入的对象
        """
        updated_list = json.dumps( obj, sort_keys=False, indent=2, ensure_ascii=False)
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(updated_list) 

    @staticmethod
    def readFile(filePath: str, encoding: str = "utf-8") -> str:
        """
        filePath: 文件路径
        encoding:文件编码
        return content 
        """
        with open(filePathth,"r",encoding=encoding) as file: 
            content=file.read() #.splitlines()# readlines() 会存在\n 
            return content
            