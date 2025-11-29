from fastapi import APIRouter, HTTPException, Body, Query
from ..models import LexRequest, LexResponse, TokenOut
from ..javalex import Lexer, LexError

router = APIRouter(prefix="/api/lex", tags=["lex"])


@router.post("", response_model=LexResponse)
def lex(req: LexRequest) -> LexResponse:
    try:
        lx = Lexer(req.code, keepСomments=req.keepСomments)
        toks = [TokenOut(**t.to_dict()) for t in lx.tokens()]
        return LexResponse(tokens=toks)
    except LexError as e:
        # Возвращаем 422 с подробностями
        raise HTTPException(
            status_code=422,
            detail={"message": e.message, "line": e.line, "column": e.column},
        )

@router.post("/text", response_model=LexResponse, summary="Lex Java from plain text")
def lex_text(
    code: str = Body(..., media_type="text/plain", description="Raw Java source (no JSON)"),
    keepСomments: bool = Query(False, description="Return comments as tokens"),
) -> LexResponse:
    try:
        lx = Lexer(code, keepСomments=keepСomments)
        toks = [TokenOut(**t.to_dict()) for t in lx.tokens()]
        return LexResponse(tokens=toks)
    except LexError as e:
        raise HTTPException(status_code=422, detail={
            "message": e.message,
            "line": e.line,
            "column": e.column
        })
