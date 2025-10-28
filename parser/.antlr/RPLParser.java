// Generated from c:/Users/KoolAid/Downloads/APL/Project/RPL/antlr_tool/RPLParser.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class RPLParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		ROLE=1, USER=2, RESOURCE=3, ALLOW=4, DENY=5, ACTION=6, ON=7, IF=8, AND=9, 
		OR=10, NOT=11, CAN=12, EQ=13, NE=14, LT=15, GT=16, LE=17, GE=18, PLUS=19, 
		MINUS=20, DIV=21, STAR=22, LPAREN=23, RPAREN=24, LBRACE=25, RBRACE=26, 
		COLON=27, COMMA=28, DOT=29, BOOLEAN=30, INTEGER=31, REAL=32, STRING=33, 
		CHARACTER=34, IDENTIFIER=35, WS=36, LINE_COMMENT=37, BLOCK_COMMENT=38;
	public static final int
		RULE_program = 0, RULE_statement = 1, RULE_roleDeclaration = 2, RULE_rolePermissions = 3, 
		RULE_permission = 4, RULE_userDeclaration = 5, RULE_userAttributes = 6, 
		RULE_userAttribute = 7, RULE_resourceDeclaration = 8, RULE_resourceAttributes = 9, 
		RULE_resourceAttribute = 10, RULE_policyRule = 11, RULE_policyType = 12, 
		RULE_actionList = 13, RULE_resourceRef = 14, RULE_ifClause = 15, RULE_condition = 16, 
		RULE_comparison = 17, RULE_comparisonOp = 18, RULE_expression = 19, RULE_memberAccess = 20, 
		RULE_value = 21;
	private static String[] makeRuleNames() {
		return new String[] {
			"program", "statement", "roleDeclaration", "rolePermissions", "permission", 
			"userDeclaration", "userAttributes", "userAttribute", "resourceDeclaration", 
			"resourceAttributes", "resourceAttribute", "policyRule", "policyType", 
			"actionList", "resourceRef", "ifClause", "condition", "comparison", "comparisonOp", 
			"expression", "memberAccess", "value"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, null, null, null, null, "'DENY'", "'action'", "'ON'", "'IF'", "'AND'", 
			"'OR'", "'NOT'", "'can'", "'=='", "'!='", "'<'", "'>'", "'<='", "'>='", 
			"'+'", "'-'", "'/'", "'*'", "'('", "')'", "'{'", "'}'", "':'", "','", 
			"'.'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "ROLE", "USER", "RESOURCE", "ALLOW", "DENY", "ACTION", "ON", "IF", 
			"AND", "OR", "NOT", "CAN", "EQ", "NE", "LT", "GT", "LE", "GE", "PLUS", 
			"MINUS", "DIV", "STAR", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COLON", 
			"COMMA", "DOT", "BOOLEAN", "INTEGER", "REAL", "STRING", "CHARACTER", 
			"IDENTIFIER", "WS", "LINE_COMMENT", "BLOCK_COMMENT"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "RPLParser.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public RPLParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProgramContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(RPLParser.EOF, 0); }
		public List<StatementContext> statement() {
			return getRuleContexts(StatementContext.class);
		}
		public StatementContext statement(int i) {
			return getRuleContext(StatementContext.class,i);
		}
		public ProgramContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_program; }
	}

	public final ProgramContext program() throws RecognitionException {
		ProgramContext _localctx = new ProgramContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_program);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(47);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 62L) != 0)) {
				{
				{
				setState(44);
				statement();
				}
				}
				setState(49);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(50);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class StatementContext extends ParserRuleContext {
		public RoleDeclarationContext roleDeclaration() {
			return getRuleContext(RoleDeclarationContext.class,0);
		}
		public UserDeclarationContext userDeclaration() {
			return getRuleContext(UserDeclarationContext.class,0);
		}
		public ResourceDeclarationContext resourceDeclaration() {
			return getRuleContext(ResourceDeclarationContext.class,0);
		}
		public PolicyRuleContext policyRule() {
			return getRuleContext(PolicyRuleContext.class,0);
		}
		public StatementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_statement; }
	}

	public final StatementContext statement() throws RecognitionException {
		StatementContext _localctx = new StatementContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_statement);
		try {
			setState(56);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ROLE:
				enterOuterAlt(_localctx, 1);
				{
				setState(52);
				roleDeclaration();
				}
				break;
			case USER:
				enterOuterAlt(_localctx, 2);
				{
				setState(53);
				userDeclaration();
				}
				break;
			case RESOURCE:
				enterOuterAlt(_localctx, 3);
				{
				setState(54);
				resourceDeclaration();
				}
				break;
			case ALLOW:
			case DENY:
				enterOuterAlt(_localctx, 4);
				{
				setState(55);
				policyRule();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RoleDeclarationContext extends ParserRuleContext {
		public TerminalNode ROLE() { return getToken(RPLParser.ROLE, 0); }
		public TerminalNode IDENTIFIER() { return getToken(RPLParser.IDENTIFIER, 0); }
		public TerminalNode LBRACE() { return getToken(RPLParser.LBRACE, 0); }
		public RolePermissionsContext rolePermissions() {
			return getRuleContext(RolePermissionsContext.class,0);
		}
		public TerminalNode RBRACE() { return getToken(RPLParser.RBRACE, 0); }
		public RoleDeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_roleDeclaration; }
	}

	public final RoleDeclarationContext roleDeclaration() throws RecognitionException {
		RoleDeclarationContext _localctx = new RoleDeclarationContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_roleDeclaration);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(58);
			match(ROLE);
			setState(59);
			match(IDENTIFIER);
			setState(60);
			match(LBRACE);
			setState(61);
			rolePermissions();
			setState(62);
			match(RBRACE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RolePermissionsContext extends ParserRuleContext {
		public TerminalNode CAN() { return getToken(RPLParser.CAN, 0); }
		public TerminalNode COLON() { return getToken(RPLParser.COLON, 0); }
		public List<PermissionContext> permission() {
			return getRuleContexts(PermissionContext.class);
		}
		public PermissionContext permission(int i) {
			return getRuleContext(PermissionContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(RPLParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(RPLParser.COMMA, i);
		}
		public RolePermissionsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rolePermissions; }
	}

	public final RolePermissionsContext rolePermissions() throws RecognitionException {
		RolePermissionsContext _localctx = new RolePermissionsContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_rolePermissions);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(64);
			match(CAN);
			setState(65);
			match(COLON);
			setState(66);
			permission();
			setState(71);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(67);
				match(COMMA);
				setState(68);
				permission();
				}
				}
				setState(73);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PermissionContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(RPLParser.IDENTIFIER, 0); }
		public TerminalNode STAR() { return getToken(RPLParser.STAR, 0); }
		public PermissionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_permission; }
	}

	public final PermissionContext permission() throws RecognitionException {
		PermissionContext _localctx = new PermissionContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_permission);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(74);
			_la = _input.LA(1);
			if ( !(_la==STAR || _la==IDENTIFIER) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class UserDeclarationContext extends ParserRuleContext {
		public TerminalNode USER() { return getToken(RPLParser.USER, 0); }
		public TerminalNode IDENTIFIER() { return getToken(RPLParser.IDENTIFIER, 0); }
		public TerminalNode LBRACE() { return getToken(RPLParser.LBRACE, 0); }
		public UserAttributesContext userAttributes() {
			return getRuleContext(UserAttributesContext.class,0);
		}
		public TerminalNode RBRACE() { return getToken(RPLParser.RBRACE, 0); }
		public UserDeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_userDeclaration; }
	}

	public final UserDeclarationContext userDeclaration() throws RecognitionException {
		UserDeclarationContext _localctx = new UserDeclarationContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_userDeclaration);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(76);
			match(USER);
			setState(77);
			match(IDENTIFIER);
			setState(78);
			match(LBRACE);
			setState(79);
			userAttributes();
			setState(80);
			match(RBRACE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class UserAttributesContext extends ParserRuleContext {
		public List<UserAttributeContext> userAttribute() {
			return getRuleContexts(UserAttributeContext.class);
		}
		public UserAttributeContext userAttribute(int i) {
			return getRuleContext(UserAttributeContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(RPLParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(RPLParser.COMMA, i);
		}
		public UserAttributesContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_userAttributes; }
	}

	public final UserAttributesContext userAttributes() throws RecognitionException {
		UserAttributesContext _localctx = new UserAttributesContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_userAttributes);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(82);
			userAttribute();
			setState(87);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(83);
				match(COMMA);
				setState(84);
				userAttribute();
				}
				}
				setState(89);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class UserAttributeContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(RPLParser.IDENTIFIER, 0); }
		public TerminalNode COLON() { return getToken(RPLParser.COLON, 0); }
		public ValueContext value() {
			return getRuleContext(ValueContext.class,0);
		}
		public UserAttributeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_userAttribute; }
	}

	public final UserAttributeContext userAttribute() throws RecognitionException {
		UserAttributeContext _localctx = new UserAttributeContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_userAttribute);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(90);
			match(IDENTIFIER);
			setState(91);
			match(COLON);
			setState(92);
			value();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ResourceDeclarationContext extends ParserRuleContext {
		public TerminalNode RESOURCE() { return getToken(RPLParser.RESOURCE, 0); }
		public TerminalNode IDENTIFIER() { return getToken(RPLParser.IDENTIFIER, 0); }
		public TerminalNode LBRACE() { return getToken(RPLParser.LBRACE, 0); }
		public ResourceAttributesContext resourceAttributes() {
			return getRuleContext(ResourceAttributesContext.class,0);
		}
		public TerminalNode RBRACE() { return getToken(RPLParser.RBRACE, 0); }
		public ResourceDeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_resourceDeclaration; }
	}

	public final ResourceDeclarationContext resourceDeclaration() throws RecognitionException {
		ResourceDeclarationContext _localctx = new ResourceDeclarationContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_resourceDeclaration);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(94);
			match(RESOURCE);
			setState(95);
			match(IDENTIFIER);
			setState(96);
			match(LBRACE);
			setState(97);
			resourceAttributes();
			setState(98);
			match(RBRACE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ResourceAttributesContext extends ParserRuleContext {
		public List<ResourceAttributeContext> resourceAttribute() {
			return getRuleContexts(ResourceAttributeContext.class);
		}
		public ResourceAttributeContext resourceAttribute(int i) {
			return getRuleContext(ResourceAttributeContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(RPLParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(RPLParser.COMMA, i);
		}
		public ResourceAttributesContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_resourceAttributes; }
	}

	public final ResourceAttributesContext resourceAttributes() throws RecognitionException {
		ResourceAttributesContext _localctx = new ResourceAttributesContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_resourceAttributes);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(100);
			resourceAttribute();
			setState(105);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(101);
				match(COMMA);
				setState(102);
				resourceAttribute();
				}
				}
				setState(107);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ResourceAttributeContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(RPLParser.IDENTIFIER, 0); }
		public TerminalNode COLON() { return getToken(RPLParser.COLON, 0); }
		public ValueContext value() {
			return getRuleContext(ValueContext.class,0);
		}
		public ResourceAttributeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_resourceAttribute; }
	}

	public final ResourceAttributeContext resourceAttribute() throws RecognitionException {
		ResourceAttributeContext _localctx = new ResourceAttributeContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_resourceAttribute);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(108);
			match(IDENTIFIER);
			setState(109);
			match(COLON);
			setState(110);
			value();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PolicyRuleContext extends ParserRuleContext {
		public PolicyTypeContext policyType() {
			return getRuleContext(PolicyTypeContext.class,0);
		}
		public TerminalNode ACTION() { return getToken(RPLParser.ACTION, 0); }
		public List<TerminalNode> COLON() { return getTokens(RPLParser.COLON); }
		public TerminalNode COLON(int i) {
			return getToken(RPLParser.COLON, i);
		}
		public ActionListContext actionList() {
			return getRuleContext(ActionListContext.class,0);
		}
		public TerminalNode ON() { return getToken(RPLParser.ON, 0); }
		public TerminalNode RESOURCE() { return getToken(RPLParser.RESOURCE, 0); }
		public ResourceRefContext resourceRef() {
			return getRuleContext(ResourceRefContext.class,0);
		}
		public IfClauseContext ifClause() {
			return getRuleContext(IfClauseContext.class,0);
		}
		public PolicyRuleContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_policyRule; }
	}

	public final PolicyRuleContext policyRule() throws RecognitionException {
		PolicyRuleContext _localctx = new PolicyRuleContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_policyRule);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(112);
			policyType();
			setState(113);
			match(ACTION);
			setState(114);
			match(COLON);
			setState(115);
			actionList();
			setState(116);
			match(ON);
			setState(117);
			match(RESOURCE);
			setState(118);
			match(COLON);
			setState(119);
			resourceRef();
			setState(121);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==IF) {
				{
				setState(120);
				ifClause();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PolicyTypeContext extends ParserRuleContext {
		public TerminalNode ALLOW() { return getToken(RPLParser.ALLOW, 0); }
		public TerminalNode DENY() { return getToken(RPLParser.DENY, 0); }
		public PolicyTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_policyType; }
	}

	public final PolicyTypeContext policyType() throws RecognitionException {
		PolicyTypeContext _localctx = new PolicyTypeContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_policyType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(123);
			_la = _input.LA(1);
			if ( !(_la==ALLOW || _la==DENY) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ActionListContext extends ParserRuleContext {
		public List<TerminalNode> IDENTIFIER() { return getTokens(RPLParser.IDENTIFIER); }
		public TerminalNode IDENTIFIER(int i) {
			return getToken(RPLParser.IDENTIFIER, i);
		}
		public List<TerminalNode> COMMA() { return getTokens(RPLParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(RPLParser.COMMA, i);
		}
		public ActionListContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_actionList; }
	}

	public final ActionListContext actionList() throws RecognitionException {
		ActionListContext _localctx = new ActionListContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_actionList);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(125);
			match(IDENTIFIER);
			setState(130);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(126);
				match(COMMA);
				setState(127);
				match(IDENTIFIER);
				}
				}
				setState(132);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ResourceRefContext extends ParserRuleContext {
		public TerminalNode IDENTIFIER() { return getToken(RPLParser.IDENTIFIER, 0); }
		public TerminalNode STRING() { return getToken(RPLParser.STRING, 0); }
		public ResourceRefContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_resourceRef; }
	}

	public final ResourceRefContext resourceRef() throws RecognitionException {
		ResourceRefContext _localctx = new ResourceRefContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_resourceRef);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(133);
			_la = _input.LA(1);
			if ( !(_la==STRING || _la==IDENTIFIER) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class IfClauseContext extends ParserRuleContext {
		public TerminalNode IF() { return getToken(RPLParser.IF, 0); }
		public ConditionContext condition() {
			return getRuleContext(ConditionContext.class,0);
		}
		public IfClauseContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ifClause; }
	}

	public final IfClauseContext ifClause() throws RecognitionException {
		IfClauseContext _localctx = new IfClauseContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_ifClause);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(135);
			match(IF);
			setState(136);
			condition(0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ConditionContext extends ParserRuleContext {
		public ConditionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_condition; }
	 
		public ConditionContext() { }
		public void copyFrom(ConditionContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class OrConditionContext extends ConditionContext {
		public List<ConditionContext> condition() {
			return getRuleContexts(ConditionContext.class);
		}
		public ConditionContext condition(int i) {
			return getRuleContext(ConditionContext.class,i);
		}
		public TerminalNode OR() { return getToken(RPLParser.OR, 0); }
		public OrConditionContext(ConditionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AndConditionContext extends ConditionContext {
		public List<ConditionContext> condition() {
			return getRuleContexts(ConditionContext.class);
		}
		public ConditionContext condition(int i) {
			return getRuleContext(ConditionContext.class,i);
		}
		public TerminalNode AND() { return getToken(RPLParser.AND, 0); }
		public AndConditionContext(ConditionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NotConditionContext extends ConditionContext {
		public TerminalNode NOT() { return getToken(RPLParser.NOT, 0); }
		public ConditionContext condition() {
			return getRuleContext(ConditionContext.class,0);
		}
		public NotConditionContext(ConditionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ParenConditionContext extends ConditionContext {
		public TerminalNode LPAREN() { return getToken(RPLParser.LPAREN, 0); }
		public ConditionContext condition() {
			return getRuleContext(ConditionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(RPLParser.RPAREN, 0); }
		public ParenConditionContext(ConditionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ComparisonConditionContext extends ConditionContext {
		public ComparisonContext comparison() {
			return getRuleContext(ComparisonContext.class,0);
		}
		public ComparisonConditionContext(ConditionContext ctx) { copyFrom(ctx); }
	}

	public final ConditionContext condition() throws RecognitionException {
		return condition(0);
	}

	private ConditionContext condition(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ConditionContext _localctx = new ConditionContext(_ctx, _parentState);
		ConditionContext _prevctx = _localctx;
		int _startState = 32;
		enterRecursionRule(_localctx, 32, RULE_condition, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(146);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,7,_ctx) ) {
			case 1:
				{
				_localctx = new NotConditionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(139);
				match(NOT);
				setState(140);
				condition(3);
				}
				break;
			case 2:
				{
				_localctx = new ParenConditionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(141);
				match(LPAREN);
				setState(142);
				condition(0);
				setState(143);
				match(RPAREN);
				}
				break;
			case 3:
				{
				_localctx = new ComparisonConditionContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(145);
				comparison();
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(156);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,9,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(154);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,8,_ctx) ) {
					case 1:
						{
						_localctx = new AndConditionContext(new ConditionContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_condition);
						setState(148);
						if (!(precpred(_ctx, 5))) throw new FailedPredicateException(this, "precpred(_ctx, 5)");
						setState(149);
						match(AND);
						setState(150);
						condition(6);
						}
						break;
					case 2:
						{
						_localctx = new OrConditionContext(new ConditionContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_condition);
						setState(151);
						if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
						setState(152);
						match(OR);
						setState(153);
						condition(5);
						}
						break;
					}
					} 
				}
				setState(158);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,9,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ComparisonContext extends ParserRuleContext {
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public ComparisonOpContext comparisonOp() {
			return getRuleContext(ComparisonOpContext.class,0);
		}
		public ComparisonContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comparison; }
	}

	public final ComparisonContext comparison() throws RecognitionException {
		ComparisonContext _localctx = new ComparisonContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_comparison);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(159);
			expression(0);
			setState(160);
			comparisonOp();
			setState(161);
			expression(0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ComparisonOpContext extends ParserRuleContext {
		public TerminalNode EQ() { return getToken(RPLParser.EQ, 0); }
		public TerminalNode NE() { return getToken(RPLParser.NE, 0); }
		public TerminalNode LT() { return getToken(RPLParser.LT, 0); }
		public TerminalNode GT() { return getToken(RPLParser.GT, 0); }
		public TerminalNode LE() { return getToken(RPLParser.LE, 0); }
		public TerminalNode GE() { return getToken(RPLParser.GE, 0); }
		public ComparisonOpContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comparisonOp; }
	}

	public final ComparisonOpContext comparisonOp() throws RecognitionException {
		ComparisonOpContext _localctx = new ComparisonOpContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_comparisonOp);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(163);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 516096L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExpressionContext extends ParserRuleContext {
		public ExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expression; }
	 
		public ExpressionContext() { }
		public void copyFrom(ExpressionContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MultiDivContext extends ExpressionContext {
		public Token op;
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public TerminalNode STAR() { return getToken(RPLParser.STAR, 0); }
		public TerminalNode DIV() { return getToken(RPLParser.DIV, 0); }
		public MultiDivContext(ExpressionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IdentifierContext extends ExpressionContext {
		public TerminalNode IDENTIFIER() { return getToken(RPLParser.IDENTIFIER, 0); }
		public IdentifierContext(ExpressionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MemberExprContext extends ExpressionContext {
		public MemberAccessContext memberAccess() {
			return getRuleContext(MemberAccessContext.class,0);
		}
		public MemberExprContext(ExpressionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AddSubContext extends ExpressionContext {
		public Token op;
		public List<ExpressionContext> expression() {
			return getRuleContexts(ExpressionContext.class);
		}
		public ExpressionContext expression(int i) {
			return getRuleContext(ExpressionContext.class,i);
		}
		public TerminalNode PLUS() { return getToken(RPLParser.PLUS, 0); }
		public TerminalNode MINUS() { return getToken(RPLParser.MINUS, 0); }
		public AddSubContext(ExpressionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IntegerContext extends ExpressionContext {
		public TerminalNode INTEGER() { return getToken(RPLParser.INTEGER, 0); }
		public IntegerContext(ExpressionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FloatContext extends ExpressionContext {
		public TerminalNode REAL() { return getToken(RPLParser.REAL, 0); }
		public FloatContext(ExpressionContext ctx) { copyFrom(ctx); }
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ParenExprContext extends ExpressionContext {
		public TerminalNode LPAREN() { return getToken(RPLParser.LPAREN, 0); }
		public ExpressionContext expression() {
			return getRuleContext(ExpressionContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(RPLParser.RPAREN, 0); }
		public ParenExprContext(ExpressionContext ctx) { copyFrom(ctx); }
	}

	public final ExpressionContext expression() throws RecognitionException {
		return expression(0);
	}

	private ExpressionContext expression(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ExpressionContext _localctx = new ExpressionContext(_ctx, _parentState);
		ExpressionContext _prevctx = _localctx;
		int _startState = 38;
		enterRecursionRule(_localctx, 38, RULE_expression, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(174);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,10,_ctx) ) {
			case 1:
				{
				_localctx = new ParenExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(166);
				match(LPAREN);
				setState(167);
				expression(0);
				setState(168);
				match(RPAREN);
				}
				break;
			case 2:
				{
				_localctx = new IntegerContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(170);
				match(INTEGER);
				}
				break;
			case 3:
				{
				_localctx = new FloatContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(171);
				match(REAL);
				}
				break;
			case 4:
				{
				_localctx = new IdentifierContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(172);
				match(IDENTIFIER);
				}
				break;
			case 5:
				{
				_localctx = new MemberExprContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(173);
				memberAccess();
				}
				break;
			}
			_ctx.stop = _input.LT(-1);
			setState(184);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,12,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(182);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,11,_ctx) ) {
					case 1:
						{
						_localctx = new MultiDivContext(new ExpressionContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(176);
						if (!(precpred(_ctx, 7))) throw new FailedPredicateException(this, "precpred(_ctx, 7)");
						setState(177);
						((MultiDivContext)_localctx).op = _input.LT(1);
						_la = _input.LA(1);
						if ( !(_la==DIV || _la==STAR) ) {
							((MultiDivContext)_localctx).op = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(178);
						expression(8);
						}
						break;
					case 2:
						{
						_localctx = new AddSubContext(new ExpressionContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expression);
						setState(179);
						if (!(precpred(_ctx, 6))) throw new FailedPredicateException(this, "precpred(_ctx, 6)");
						setState(180);
						((AddSubContext)_localctx).op = _input.LT(1);
						_la = _input.LA(1);
						if ( !(_la==PLUS || _la==MINUS) ) {
							((AddSubContext)_localctx).op = (Token)_errHandler.recoverInline(this);
						}
						else {
							if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
							_errHandler.reportMatch(this);
							consume();
						}
						setState(181);
						expression(7);
						}
						break;
					}
					} 
				}
				setState(186);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,12,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class MemberAccessContext extends ParserRuleContext {
		public List<TerminalNode> IDENTIFIER() { return getTokens(RPLParser.IDENTIFIER); }
		public TerminalNode IDENTIFIER(int i) {
			return getToken(RPLParser.IDENTIFIER, i);
		}
		public TerminalNode DOT() { return getToken(RPLParser.DOT, 0); }
		public MemberAccessContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_memberAccess; }
	}

	public final MemberAccessContext memberAccess() throws RecognitionException {
		MemberAccessContext _localctx = new MemberAccessContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_memberAccess);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(187);
			match(IDENTIFIER);
			setState(188);
			match(DOT);
			setState(189);
			match(IDENTIFIER);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ValueContext extends ParserRuleContext {
		public TerminalNode STRING() { return getToken(RPLParser.STRING, 0); }
		public TerminalNode CHARACTER() { return getToken(RPLParser.CHARACTER, 0); }
		public TerminalNode INTEGER() { return getToken(RPLParser.INTEGER, 0); }
		public TerminalNode REAL() { return getToken(RPLParser.REAL, 0); }
		public TerminalNode IDENTIFIER() { return getToken(RPLParser.IDENTIFIER, 0); }
		public TerminalNode BOOLEAN() { return getToken(RPLParser.BOOLEAN, 0); }
		public ValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_value; }
	}

	public final ValueContext value() throws RecognitionException {
		ValueContext _localctx = new ValueContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_value);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(191);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 67645734912L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 16:
			return condition_sempred((ConditionContext)_localctx, predIndex);
		case 19:
			return expression_sempred((ExpressionContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean condition_sempred(ConditionContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 5);
		case 1:
			return precpred(_ctx, 4);
		}
		return true;
	}
	private boolean expression_sempred(ExpressionContext _localctx, int predIndex) {
		switch (predIndex) {
		case 2:
			return precpred(_ctx, 7);
		case 3:
			return precpred(_ctx, 6);
		}
		return true;
	}

	public static final String _serializedATN =
		"\u0004\u0001&\u00c2\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007\u000f"+
		"\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002\u0012\u0007\u0012"+
		"\u0002\u0013\u0007\u0013\u0002\u0014\u0007\u0014\u0002\u0015\u0007\u0015"+
		"\u0001\u0000\u0005\u0000.\b\u0000\n\u0000\f\u00001\t\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0003\u0001"+
		"9\b\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002"+
		"\u0001\u0002\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003"+
		"\u0005\u0003F\b\u0003\n\u0003\f\u0003I\t\u0003\u0001\u0004\u0001\u0004"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0006\u0001\u0006\u0001\u0006\u0005\u0006V\b\u0006\n\u0006\f\u0006"+
		"Y\t\u0006\u0001\u0007\u0001\u0007\u0001\u0007\u0001\u0007\u0001\b\u0001"+
		"\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\t\u0001\t\u0001\t\u0005\th\b"+
		"\t\n\t\f\tk\t\t\u0001\n\u0001\n\u0001\n\u0001\n\u0001\u000b\u0001\u000b"+
		"\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b"+
		"\u0001\u000b\u0003\u000bz\b\u000b\u0001\f\u0001\f\u0001\r\u0001\r\u0001"+
		"\r\u0005\r\u0081\b\r\n\r\f\r\u0084\t\r\u0001\u000e\u0001\u000e\u0001\u000f"+
		"\u0001\u000f\u0001\u000f\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010"+
		"\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0003\u0010\u0093\b\u0010"+
		"\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010"+
		"\u0005\u0010\u009b\b\u0010\n\u0010\f\u0010\u009e\t\u0010\u0001\u0011\u0001"+
		"\u0011\u0001\u0011\u0001\u0011\u0001\u0012\u0001\u0012\u0001\u0013\u0001"+
		"\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0001"+
		"\u0013\u0001\u0013\u0003\u0013\u00af\b\u0013\u0001\u0013\u0001\u0013\u0001"+
		"\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0005\u0013\u00b7\b\u0013\n"+
		"\u0013\f\u0013\u00ba\t\u0013\u0001\u0014\u0001\u0014\u0001\u0014\u0001"+
		"\u0014\u0001\u0015\u0001\u0015\u0001\u0015\u0000\u0002 &\u0016\u0000\u0002"+
		"\u0004\u0006\b\n\f\u000e\u0010\u0012\u0014\u0016\u0018\u001a\u001c\u001e"+
		" \"$&(*\u0000\u0007\u0002\u0000\u0016\u0016##\u0001\u0000\u0004\u0005"+
		"\u0002\u0000!!##\u0001\u0000\r\u0012\u0001\u0000\u0015\u0016\u0001\u0000"+
		"\u0013\u0014\u0001\u0000\u001e#\u00be\u0000/\u0001\u0000\u0000\u0000\u0002"+
		"8\u0001\u0000\u0000\u0000\u0004:\u0001\u0000\u0000\u0000\u0006@\u0001"+
		"\u0000\u0000\u0000\bJ\u0001\u0000\u0000\u0000\nL\u0001\u0000\u0000\u0000"+
		"\fR\u0001\u0000\u0000\u0000\u000eZ\u0001\u0000\u0000\u0000\u0010^\u0001"+
		"\u0000\u0000\u0000\u0012d\u0001\u0000\u0000\u0000\u0014l\u0001\u0000\u0000"+
		"\u0000\u0016p\u0001\u0000\u0000\u0000\u0018{\u0001\u0000\u0000\u0000\u001a"+
		"}\u0001\u0000\u0000\u0000\u001c\u0085\u0001\u0000\u0000\u0000\u001e\u0087"+
		"\u0001\u0000\u0000\u0000 \u0092\u0001\u0000\u0000\u0000\"\u009f\u0001"+
		"\u0000\u0000\u0000$\u00a3\u0001\u0000\u0000\u0000&\u00ae\u0001\u0000\u0000"+
		"\u0000(\u00bb\u0001\u0000\u0000\u0000*\u00bf\u0001\u0000\u0000\u0000,"+
		".\u0003\u0002\u0001\u0000-,\u0001\u0000\u0000\u0000.1\u0001\u0000\u0000"+
		"\u0000/-\u0001\u0000\u0000\u0000/0\u0001\u0000\u0000\u000002\u0001\u0000"+
		"\u0000\u00001/\u0001\u0000\u0000\u000023\u0005\u0000\u0000\u00013\u0001"+
		"\u0001\u0000\u0000\u000049\u0003\u0004\u0002\u000059\u0003\n\u0005\u0000"+
		"69\u0003\u0010\b\u000079\u0003\u0016\u000b\u000084\u0001\u0000\u0000\u0000"+
		"85\u0001\u0000\u0000\u000086\u0001\u0000\u0000\u000087\u0001\u0000\u0000"+
		"\u00009\u0003\u0001\u0000\u0000\u0000:;\u0005\u0001\u0000\u0000;<\u0005"+
		"#\u0000\u0000<=\u0005\u0019\u0000\u0000=>\u0003\u0006\u0003\u0000>?\u0005"+
		"\u001a\u0000\u0000?\u0005\u0001\u0000\u0000\u0000@A\u0005\f\u0000\u0000"+
		"AB\u0005\u001b\u0000\u0000BG\u0003\b\u0004\u0000CD\u0005\u001c\u0000\u0000"+
		"DF\u0003\b\u0004\u0000EC\u0001\u0000\u0000\u0000FI\u0001\u0000\u0000\u0000"+
		"GE\u0001\u0000\u0000\u0000GH\u0001\u0000\u0000\u0000H\u0007\u0001\u0000"+
		"\u0000\u0000IG\u0001\u0000\u0000\u0000JK\u0007\u0000\u0000\u0000K\t\u0001"+
		"\u0000\u0000\u0000LM\u0005\u0002\u0000\u0000MN\u0005#\u0000\u0000NO\u0005"+
		"\u0019\u0000\u0000OP\u0003\f\u0006\u0000PQ\u0005\u001a\u0000\u0000Q\u000b"+
		"\u0001\u0000\u0000\u0000RW\u0003\u000e\u0007\u0000ST\u0005\u001c\u0000"+
		"\u0000TV\u0003\u000e\u0007\u0000US\u0001\u0000\u0000\u0000VY\u0001\u0000"+
		"\u0000\u0000WU\u0001\u0000\u0000\u0000WX\u0001\u0000\u0000\u0000X\r\u0001"+
		"\u0000\u0000\u0000YW\u0001\u0000\u0000\u0000Z[\u0005#\u0000\u0000[\\\u0005"+
		"\u001b\u0000\u0000\\]\u0003*\u0015\u0000]\u000f\u0001\u0000\u0000\u0000"+
		"^_\u0005\u0003\u0000\u0000_`\u0005#\u0000\u0000`a\u0005\u0019\u0000\u0000"+
		"ab\u0003\u0012\t\u0000bc\u0005\u001a\u0000\u0000c\u0011\u0001\u0000\u0000"+
		"\u0000di\u0003\u0014\n\u0000ef\u0005\u001c\u0000\u0000fh\u0003\u0014\n"+
		"\u0000ge\u0001\u0000\u0000\u0000hk\u0001\u0000\u0000\u0000ig\u0001\u0000"+
		"\u0000\u0000ij\u0001\u0000\u0000\u0000j\u0013\u0001\u0000\u0000\u0000"+
		"ki\u0001\u0000\u0000\u0000lm\u0005#\u0000\u0000mn\u0005\u001b\u0000\u0000"+
		"no\u0003*\u0015\u0000o\u0015\u0001\u0000\u0000\u0000pq\u0003\u0018\f\u0000"+
		"qr\u0005\u0006\u0000\u0000rs\u0005\u001b\u0000\u0000st\u0003\u001a\r\u0000"+
		"tu\u0005\u0007\u0000\u0000uv\u0005\u0003\u0000\u0000vw\u0005\u001b\u0000"+
		"\u0000wy\u0003\u001c\u000e\u0000xz\u0003\u001e\u000f\u0000yx\u0001\u0000"+
		"\u0000\u0000yz\u0001\u0000\u0000\u0000z\u0017\u0001\u0000\u0000\u0000"+
		"{|\u0007\u0001\u0000\u0000|\u0019\u0001\u0000\u0000\u0000}\u0082\u0005"+
		"#\u0000\u0000~\u007f\u0005\u001c\u0000\u0000\u007f\u0081\u0005#\u0000"+
		"\u0000\u0080~\u0001\u0000\u0000\u0000\u0081\u0084\u0001\u0000\u0000\u0000"+
		"\u0082\u0080\u0001\u0000\u0000\u0000\u0082\u0083\u0001\u0000\u0000\u0000"+
		"\u0083\u001b\u0001\u0000\u0000\u0000\u0084\u0082\u0001\u0000\u0000\u0000"+
		"\u0085\u0086\u0007\u0002\u0000\u0000\u0086\u001d\u0001\u0000\u0000\u0000"+
		"\u0087\u0088\u0005\b\u0000\u0000\u0088\u0089\u0003 \u0010\u0000\u0089"+
		"\u001f\u0001\u0000\u0000\u0000\u008a\u008b\u0006\u0010\uffff\uffff\u0000"+
		"\u008b\u008c\u0005\u000b\u0000\u0000\u008c\u0093\u0003 \u0010\u0003\u008d"+
		"\u008e\u0005\u0017\u0000\u0000\u008e\u008f\u0003 \u0010\u0000\u008f\u0090"+
		"\u0005\u0018\u0000\u0000\u0090\u0093\u0001\u0000\u0000\u0000\u0091\u0093"+
		"\u0003\"\u0011\u0000\u0092\u008a\u0001\u0000\u0000\u0000\u0092\u008d\u0001"+
		"\u0000\u0000\u0000\u0092\u0091\u0001\u0000\u0000\u0000\u0093\u009c\u0001"+
		"\u0000\u0000\u0000\u0094\u0095\n\u0005\u0000\u0000\u0095\u0096\u0005\t"+
		"\u0000\u0000\u0096\u009b\u0003 \u0010\u0006\u0097\u0098\n\u0004\u0000"+
		"\u0000\u0098\u0099\u0005\n\u0000\u0000\u0099\u009b\u0003 \u0010\u0005"+
		"\u009a\u0094\u0001\u0000\u0000\u0000\u009a\u0097\u0001\u0000\u0000\u0000"+
		"\u009b\u009e\u0001\u0000\u0000\u0000\u009c\u009a\u0001\u0000\u0000\u0000"+
		"\u009c\u009d\u0001\u0000\u0000\u0000\u009d!\u0001\u0000\u0000\u0000\u009e"+
		"\u009c\u0001\u0000\u0000\u0000\u009f\u00a0\u0003&\u0013\u0000\u00a0\u00a1"+
		"\u0003$\u0012\u0000\u00a1\u00a2\u0003&\u0013\u0000\u00a2#\u0001\u0000"+
		"\u0000\u0000\u00a3\u00a4\u0007\u0003\u0000\u0000\u00a4%\u0001\u0000\u0000"+
		"\u0000\u00a5\u00a6\u0006\u0013\uffff\uffff\u0000\u00a6\u00a7\u0005\u0017"+
		"\u0000\u0000\u00a7\u00a8\u0003&\u0013\u0000\u00a8\u00a9\u0005\u0018\u0000"+
		"\u0000\u00a9\u00af\u0001\u0000\u0000\u0000\u00aa\u00af\u0005\u001f\u0000"+
		"\u0000\u00ab\u00af\u0005 \u0000\u0000\u00ac\u00af\u0005#\u0000\u0000\u00ad"+
		"\u00af\u0003(\u0014\u0000\u00ae\u00a5\u0001\u0000\u0000\u0000\u00ae\u00aa"+
		"\u0001\u0000\u0000\u0000\u00ae\u00ab\u0001\u0000\u0000\u0000\u00ae\u00ac"+
		"\u0001\u0000\u0000\u0000\u00ae\u00ad\u0001\u0000\u0000\u0000\u00af\u00b8"+
		"\u0001\u0000\u0000\u0000\u00b0\u00b1\n\u0007\u0000\u0000\u00b1\u00b2\u0007"+
		"\u0004\u0000\u0000\u00b2\u00b7\u0003&\u0013\b\u00b3\u00b4\n\u0006\u0000"+
		"\u0000\u00b4\u00b5\u0007\u0005\u0000\u0000\u00b5\u00b7\u0003&\u0013\u0007"+
		"\u00b6\u00b0\u0001\u0000\u0000\u0000\u00b6\u00b3\u0001\u0000\u0000\u0000"+
		"\u00b7\u00ba\u0001\u0000\u0000\u0000\u00b8\u00b6\u0001\u0000\u0000\u0000"+
		"\u00b8\u00b9\u0001\u0000\u0000\u0000\u00b9\'\u0001\u0000\u0000\u0000\u00ba"+
		"\u00b8\u0001\u0000\u0000\u0000\u00bb\u00bc\u0005#\u0000\u0000\u00bc\u00bd"+
		"\u0005\u001d\u0000\u0000\u00bd\u00be\u0005#\u0000\u0000\u00be)\u0001\u0000"+
		"\u0000\u0000\u00bf\u00c0\u0007\u0006\u0000\u0000\u00c0+\u0001\u0000\u0000"+
		"\u0000\r/8GWiy\u0082\u0092\u009a\u009c\u00ae\u00b6\u00b8";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}