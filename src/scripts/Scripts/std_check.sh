PROJ_PATH=$1
RED='\033[0;31m'
GRE='\033[0;32m'
NC='\033[0m'
ER=0
a=1

if !([ -d "$PROJ_PATH" ])
then 
    ER=$a
    echo -e "${RED}Error: Directory $PROJ_PATH does not exists.${NC}"
else
    echo "Directory $PROJ_PATH exists." 
fi

if !([ -f "$PROJ_PATH/metadata.yaml" ])
then 
    ER=$a
    echo -e "      ${RED}Error: File $PROJ_PATH/metadata.yaml does not exists.${NC}"
else    
    echo "      File $PROJ_PATH/metadata.yaml exists." 
fi

if !([ -d "$PROJ_PATH/src" ])
then 
    ER=$a
    echo -e "${RED}Error: Directory $PROJ_PATH/src does not exists.${NC}"
else    
    echo "Directory $PROJ_PATH/src exists."
fi

if !([ -f "$PROJ_PATH/src/model.py" ])
then 
    ER=$a
    echo -e "     ${RED}Error: File $PROJ_PATH/src/model.py does not exists.${NC}"
else    
    echo "      File $PROJ_PATH/src/model.py exists."
fi
if !([ -f "$PROJ_PATH/src/__init__.py" ])
then 
    ER=$a
    echo -e "      ${RED}Error: File $PROJ_PATH/src/__init__.py does not exists.${NC}"
else    
    echo "      File $PROJ_PATH/src/__init__.py exists." 
fi



if !([ -d "$PROJ_PATH/notebooks" ])
then 
    ER=$a
    echo -e "${RED}Error: Directory $PROJ_PATH/notebooks does not exists.${NC}"
else
    echo "Directory $PROJ_PATH/notebooks exists."
fi

printf "\n"
if [ $ER == 1 ]
then
    echo -e "${RED}Error: Project Structure has been changed, please fix it \n${NC}"
    exit 0
else
    echo -e "${GRE}Project structure is ok \n${NC}"

fi


if ! black ./$PROJ_PATH --check; then
    echo -e "${RED}Please run the command 'black' to format your files"
    exit 0
else
    echo -e "${GRE}Files formated, moving foward"
fi


