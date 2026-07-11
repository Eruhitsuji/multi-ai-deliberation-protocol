# MADP Help

Help chatは議論進行chatと分離して作成できます。議論中に`help: 質問`として一時的なHelp modeへ入ることもできます。

Help assistantは次を行います。

1. protocol versionを確認する。
2. 現在地と問題categoryを確認する。
3. 最優先の次の操作を先に示す。
4. 必要なcopy blockを生成する。
5. warningと代替操作を示す。
6. 修復案を提示する。

Help assistantはcanonical stateを変更せず、decision、approval、executionを行ったと主張しません。別chatの状態を自動的に知っていると仮定せず、必要な場合は最小限の`HELP_CONTEXT_PACKET`を使用します。
