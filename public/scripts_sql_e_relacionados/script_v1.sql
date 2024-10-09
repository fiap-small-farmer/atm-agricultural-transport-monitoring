CREATE TABLE Produto (
    ID_Produto INT PRIMARY KEY,
    Produto VARCHAR2(50),
    Quantidade INT,
    Unidade_Transporte VARCHAR2(20),
    Temperatura_Minima NUMBER(5,2),
    Temperatura_Maxima NUMBER(5,2),
    Instrucoes VARCHAR2(255),
    Tipo_Caminhão VARCHAR2(20)
);

CREATE TABLE Origem (
    ID_Origem INT PRIMARY KEY,
    Nome_Produtora VARCHAR2(50),
    CEP VARCHAR2(9),
    Endereço VARCHAR2(100),
    Número INT,
    Bairro VARCHAR2(50),
    Cidade VARCHAR2(50),
    Estado VARCHAR2(2)
);

CREATE TABLE Destino (
    ID_Destino INT PRIMARY KEY,
    Nome_Comprador VARCHAR2(50),
    CEP VARCHAR2(9),
    Endereço VARCHAR2(100),
    Número INT,
    Bairro VARCHAR2(50),
    Cidade VARCHAR2(50),
    Estado VARCHAR2(2)
);

CREATE TABLE Transporte (
    ID_Transporte INT PRIMARY KEY,
    ID_Produto INT,
    ID_Origem INT,
    ID_Destino INT,
    Status_Transporte VARCHAR2(20),
    Temperatura_Monitorada NUMBER(5,2),
    FOREIGN KEY (ID_Produto) REFERENCES Produto(ID_Produto),
    FOREIGN KEY (ID_Origem) REFERENCES Origem(ID_Origem),
    FOREIGN KEY (ID_Destino) REFERENCES Destino(ID_Destino)
);
