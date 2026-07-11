# alpha.2からalpha.3への移行（参考訳）

移行はalpha.2 command名、session ID、state version、decision revisionを保持し、authorityを増加させません。成功だけでなくFAILED・QUARANTINEDも記録でき、source保存やrollback不可を事実として明示します。
