from fastapi import APIRouter, HTTPException
from ..models import LexRequest, LexResponse, TokenOut
from ..javalex import Lexer, LexError

router = APIRouter(prefix="/api/lex", tags=["lex"])


@router.post("", response_model=LexResponse)
def lex(req: LexRequest) -> LexResponse:
    try:
        lx = Lexer(req.code, keep_comments=req.keep_comments)
        toks = [TokenOut(**t.to_dict()) for t in lx.tokens()]
        return LexResponse(tokens=toks)
    except LexError as e:
        # Возвращаем 422 с подробностями
        raise HTTPException(
            status_code=422,
            detail={"message": e.message, "line": e.line, "column": e.column},
        )
