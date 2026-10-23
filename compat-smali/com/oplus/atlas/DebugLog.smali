# From OnePlus 15 ColorOS 17.0.0.102 IN oplus-framework.jar.
# Framework-only hidden-API access-list flags removed for app DEX assembly.
.class public final Lcom/oplus/atlas/DebugLog;
.super Ljava/lang/Object;
.source "DebugLog.java"


# static fields
.field private static final DEBUG_MODE:Z

.field private static final LOGD:Z = true

.field private static final LOGE:Z = true

.field private static final LOGI:Z = true

.field private static final LOGV:Z = true

.field private static final LOGW:Z = true

.field private static final SHOWDETAILINFO:Z = false


# direct methods
.method static constructor <clinit>()V
    .locals 2

    .line 29
    const-string/jumbo v0, "persist.sys.assert.panic"

    const/4 v1, 0x0

    invoke-static {v0, v1}, Landroid/os/SystemProperties;->getBoolean(Ljava/lang/String;Z)Z

    move-result v0

    sput-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .line 22
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static d(Ljava/lang/String;Ljava/lang/String;)I
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;

    .line 71
    sget-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    if-eqz v0, :cond_0

    .line 76
    invoke-static {p0, p1}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    move-result v0

    return v0

    .line 79
    :cond_0
    const/4 v0, -0x1

    return v0
.end method

.method public static d(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;
    .param p2, "tr"    # Ljava/lang/Throwable;

    .line 97
    sget-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    if-eqz v0, :cond_0

    .line 102
    invoke-static {p0, p1, p2}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    move-result v0

    return v0

    .line 105
    :cond_0
    const/4 v0, -0x1

    return v0
.end method

.method public static d(Ljava/lang/String;ZLjava/lang/String;)I
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "debug"    # Z
    .param p2, "msg"    # Ljava/lang/String;

    .line 84
    if-eqz p1, :cond_0

    sget-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    if-eqz v0, :cond_0

    .line 89
    invoke-static {p0, p2}, Lcom/oplus/atlas/DebugLog;->d(Ljava/lang/String;Ljava/lang/String;)I

    move-result v0

    return v0

    .line 92
    :cond_0
    const/4 v0, -0x1

    return v0
.end method

.method public static e(Ljava/lang/String;Ljava/lang/String;)I
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;

    .line 162
    sget-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    if-eqz v0, :cond_0

    .line 167
    invoke-static {p0, p1}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

    move-result v0

    return v0

    .line 170
    :cond_0
    const/4 v0, -0x1

    return v0
.end method

.method public static e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;
    .param p2, "tr"    # Ljava/lang/Throwable;

    .line 175
    sget-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    if-eqz v0, :cond_0

    .line 180
    invoke-static {p0, p1, p2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    move-result v0

    return v0

    .line 183
    :cond_0
    const/4 v0, -0x1

    return v0
.end method

.method private static getFunctionName()Ljava/lang/String;
    .locals 7

    .line 188
    invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/Thread;->getStackTrace()[Ljava/lang/StackTraceElement;

    move-result-object v0

    .line 189
    .local v0, "sts":[Ljava/lang/StackTraceElement;
    const/4 v1, 0x0

    if-nez v0, :cond_0

    .line 190
    return-object v1

    .line 192
    :cond_0
    array-length v2, v0

    const/4 v3, 0x0

    :goto_0
    if-ge v3, v2, :cond_4

    aget-object v4, v0, v3

    .line 193
    .local v4, "st":Ljava/lang/StackTraceElement;
    invoke-virtual {v4}, Ljava/lang/StackTraceElement;->isNativeMethod()Z

    move-result v5

    if-eqz v5, :cond_1

    .line 194
    goto :goto_1

    .line 196
    :cond_1
    invoke-virtual {v4}, Ljava/lang/StackTraceElement;->getClassName()Ljava/lang/String;

    move-result-object v5

    const-class v6, Ljava/lang/Thread;

    invoke-virtual {v6}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/Object;->equals(Ljava/lang/Object;)Z

    move-result v5

    if-eqz v5, :cond_2

    .line 197
    goto :goto_1

    .line 199
    :cond_2
    invoke-virtual {v4}, Ljava/lang/StackTraceElement;->getClassName()Ljava/lang/String;

    move-result-object v5

    const-class v6, Lcom/oplus/atlas/DebugLog;

    invoke-virtual {v6}, Ljava/lang/Class;->getName()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/Object;->equals(Ljava/lang/Object;)Z

    move-result v5

    if-eqz v5, :cond_3

    .line 200
    nop

    .line 192
    .end local v4    # "st":Ljava/lang/StackTraceElement;
    :goto_1
    add-int/lit8 v3, v3, 0x1

    goto :goto_0

    .line 202
    .restart local v4    # "st":Ljava/lang/StackTraceElement;
    :cond_3
    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "[ "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-static {}, Ljava/lang/Thread;->currentThread()Ljava/lang/Thread;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/Thread;->getName()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ": "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v4}, Ljava/lang/StackTraceElement;->getLineNumber()I

    move-result v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, " "

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    .line 203
    invoke-virtual {v4}, Ljava/lang/StackTraceElement;->getMethodName()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, " ]"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    .line 202
    return-object v1

    .line 205
    .end local v4    # "st":Ljava/lang/StackTraceElement;
    :cond_4
    return-object v1
.end method

.method public static i(Ljava/lang/String;Ljava/lang/String;)I
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;

    .line 110
    sget-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    if-eqz v0, :cond_0

    .line 115
    invoke-static {p0, p1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    move-result v0

    return v0

    .line 118
    :cond_0
    const/4 v0, -0x1

    return v0
.end method

.method public static i(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;
    .param p2, "tr"    # Ljava/lang/Throwable;

    .line 123
    sget-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    if-eqz v0, :cond_0

    .line 128
    invoke-static {p0, p1, p2}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    move-result v0

    return v0

    .line 131
    :cond_0
    const/4 v0, -0x1

    return v0
.end method

.method public static v(Ljava/lang/String;Ljava/lang/String;)I
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;

    .line 32
    sget-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    if-eqz v0, :cond_0

    .line 37
    invoke-static {p0, p1}, Landroid/util/Log;->v(Ljava/lang/String;Ljava/lang/String;)I

    move-result v0

    return v0

    .line 40
    :cond_0
    const/4 v0, -0x1

    return v0
.end method

.method public static v(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;
    .param p2, "tr"    # Ljava/lang/Throwable;

    .line 45
    sget-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    if-eqz v0, :cond_0

    .line 50
    invoke-static {p0, p1, p2}, Landroid/util/Log;->v(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    move-result v0

    return v0

    .line 53
    :cond_0
    const/4 v0, -0x1

    return v0
.end method

.method public static v(Ljava/lang/String;ZLjava/lang/String;)I
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "debug"    # Z
    .param p2, "msg"    # Ljava/lang/String;

    .line 58
    if-eqz p1, :cond_0

    sget-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    if-eqz v0, :cond_0

    .line 63
    invoke-static {p0, p2}, Lcom/oplus/atlas/DebugLog;->v(Ljava/lang/String;Ljava/lang/String;)I

    move-result v0

    return v0

    .line 66
    :cond_0
    const/4 v0, -0x1

    return v0
.end method

.method public static w(Ljava/lang/String;Ljava/lang/String;)I
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;

    .line 136
    sget-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    if-eqz v0, :cond_0

    .line 141
    invoke-static {p0, p1}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;)I

    move-result v0

    return v0

    .line 144
    :cond_0
    const/4 v0, -0x1

    return v0
.end method

.method public static w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I
    .locals 1
    .param p0, "tag"    # Ljava/lang/String;
    .param p1, "msg"    # Ljava/lang/String;
    .param p2, "tr"    # Ljava/lang/Throwable;

    .line 149
    sget-boolean v0, Lcom/oplus/atlas/DebugLog;->DEBUG_MODE:Z

    if-eqz v0, :cond_0

    .line 154
    invoke-static {p0, p1, p2}, Landroid/util/Log;->w(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I

    move-result v0

    return v0

    .line 157
    :cond_0
    const/4 v0, -0x1

    return v0
.end method
